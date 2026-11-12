table.unpack = table.unpack or unpack -- Compatibility for the existing test mock.
-- Native-frame mock smoke test; not a replacement for a Retail client test.
local root = "MusicSCAN/"
for _, name in ipairs({"Database.lua", "MusicSCAN.lua", "UI.lua"}) do
    assert(loadfile(root .. name), "parse failed: " .. name)
end

local clock, frames, engineCalls, messages = 100, {}, {}, {}
local cvars = { Sound_EnableAllSound = true, Sound_EnableMusic = true }
local musicAccepted, musicThrows = true, false
local timers = {}
C_Timer = {}
function C_Timer.NewTimer(delay, callback)
    local timer = { due=clock+delay, callback=callback, canceled=false, fired=false }
    function timer:Cancel() self.canceled=true end
    timers[#timers+1]=timer
    return timer
end
local function Advance(seconds)
    clock=clock+seconds
    for _,timer in ipairs(timers) do
        if not timer.canceled and not timer.fired and timer.due<=clock then
            timer.fired=true
            timer.callback()
        end
    end
end
local function PendingTimers()
    local count=0
    for _,timer in ipairs(timers) do
        if not timer.canceled and not timer.fired then count=count+1 end
    end
    return count
end
local M = {}
local function noop() end
for _, name in ipairs({
    "SetBackdrop", "SetBackdropColor", "SetBackdropBorderColor", "SetFont",
    "SetTextColor", "SetJustifyH", "SetColorTexture", "SetTexture", "SetTexCoord",
    "SetNormalTexture", "SetPushedTexture", "SetFrameStrata", "SetToplevel", "SetMovable", "SetClampedToScreen",
    "EnableMouse", "RegisterForClicks", "RegisterForDrag", "SetHighlightTexture",
    "SetTextInsets", "SetAutoFocus", "SetMaxLetters", "SetWordWrap", "SetStatusBarTexture",
    "SetStatusBarColor", "SetScrollChild", "SetOwner", "AddLine",
}) do M[name] = noop end
function M:SetOwner(owner, anchor) self.owner, self.ownerAnchor = owner, anchor end
function M:SetClampedToScreen(value) self.clampedToScreen = value end
function M:SetAtlas(atlas) self.atlas=atlas end
function M:SetAlpha(value) self.alpha=value end
function M:SetVertexColor(r,g,b) self.vertexColor={r,g,b} end
function M:SetTextColor(r,g,b) self.textColor = {r,g,b} end
function M:AddLine(text) self.tooltipLines = self.tooltipLines or {}; table.insert(self.tooltipLines,text) end
function M:SetScript(event, fn) self.scripts[event] = fn end
function M:HookScript(event, fn)
    local old = self.scripts[event]
    self.scripts[event] = function(...) if old then old(...) end; fn(...) end
end
function M:RegisterEvent(event) self.events[event] = true end
function M:UnregisterEvent(event) self.events[event] = nil end
function M:SetSize(w,h)
    local changed = self.width ~= w or self.height ~= h
    self.width, self.height = w,h
    if changed and self.scripts.OnSizeChanged then self.scripts.OnSizeChanged(self,w,h) end
end
function M:SetResizable(value) self.resizable = value end
function M:SetResizeBounds(...) self.resizeBounds = {...} end
function M:StartSizing(point)
    assert(self.resizable, "frame must enable resizing")
    self.sizing = point
end
function M:SetWidth(w) self.width = w end
function M:SetHeight(h) self.height = h end
function M:GetWidth() return self.width or 100 end
function M:GetHeight() return self.height or 150 end
function M:SetPoint(point, a,b,c,d)
    self.anchors = self.anchors or {}
    self.anchors[point] = {point,a,b,c,d}
    if type(a) == "number" then self.point = {point, self.parent, point, a,b}
    else self.point = {point, a or self.parent, b or point, c or 0,d or 0} end
end
function M:GetPoint() return table.unpack(self.point or {"CENTER", UIParent, "CENTER", 0,0}) end
function M:ClearAllPoints() self.point = nil; self.anchors = {} end
function M:SetAllPoints() end
function M:SetFrameLevel(n) self.level = n end
function M:GetFrameLevel() return self.level or 1 end
function M:GetEffectiveScale() return 1 end
function M:GetCenter() return 500,500 end
function M:IsMouseOver() return self.mouseOver == true end
function M:IsShown() return self.shown end
function M:SetShown(value)
    value = not not value
    if self.shown == value then return end
    self.shown = value
    local fn = self.scripts[value and "OnShow" or "OnHide"]
    if fn then fn(self) end
end
function M:Show() self:SetShown(true) end
function M:Hide() self:SetShown(false) end
function M:SetEnabled(value)
    value = not not value
    if self.enabled == value then return end
    self.enabled = value
    local fn = self.scripts[value and "OnEnable" or "OnDisable"]
    if fn then fn(self) end
end
function M:IsEnabled() return self.enabled end
function M:Disable() self:SetEnabled(false) end
function M:SetChecked(v) self.checked = v end
function M:GetChecked() return self.checked end
function M:SetText(t)
    self.textValue = t
    self.tooltipLines = {}
    if self.scripts.OnTextChanged then self.scripts.OnTextChanged(self) end
end
function M:GetText() return self.textValue or "" end
function M:ClearFocus() self.focus = false end
function M:StartMoving() self.moving = true end
function M:StopMovingOrSizing() self.moving = false; self.sizing = nil end
function M:SetVerticalScroll(value)
    local changed = self.vertical ~= value
    self.vertical = value
    if changed and self.scripts.OnVerticalScroll then self.scripts.OnVerticalScroll(self,value) end
end
function M:GetVerticalScroll() return self.vertical or 0 end
function M:SetMinMaxValues(a,b) self.min, self.max = a,b end
function M:SetValue(v) self.value = v end
function M:CreateTexture() return CreateFrame("Texture", nil, self) end
function M:CreateFontString() return CreateFrame("FontString", nil, self) end
function CreateFrame(kind, name, parent, template)
    local f = setmetatable({kind=kind, name=name, parent=parent, template=template,
        scripts={}, events={}, shown=true, enabled=true}, {__index=M})
    frames[#frames+1] = f
    if name then _G[name] = f end
    return f
end
UIParent = CreateFrame("Frame", "UIParent")
UIParent:SetSize(1920,1080)
Minimap = CreateFrame("Frame", "Minimap", UIParent)
Minimap:SetSize(140,140)
GameTooltip = CreateFrame("Tooltip")
STANDARD_TEXT_FONT = "Fonts\\FRIZQT__.TTF"
RAID_CLASS_COLORS = {MONK={r=0,g=1,b=152/255}}
UISpecialFrames, SlashCmdList = {}, {}
C_CVar = {GetCVarBool=function(name) return cvars[name] end}
local clockReads = 0
GetTime = function() clockReads = clockReads + 1; return clock end
GetCursorPosition = function() return 600,500 end
math.atan2 = function(y,x) return math.atan(y,x) end -- WoW Lua 5.1 extension
PlayMusic = function(id) engineCalls[#engineCalls+1] = {"play",id}; if musicThrows then error("Audio unavailable") end; return musicAccepted end
StopMusic = function() engineCalls[#engineCalls+1] = {"stop"} end
print = function(s) messages[#messages+1] = s end


-- A removed selection must fall back; removed-but-valid Favorite IDs must survive.
MusicSCANDB = {
    selectedTrack="wod-frostfire-magnificent-desolation-h",
    favorites={[936340]=true,[8158670]=true,[999999999]=true,[-1]=true,bad=true},
    window={width=640,height=600,point="TOPLEFT",relativePoint="TOPLEFT",x=35,y=-60,visible=true},
    minimap={angle=42}, collapsedExpansions={Shadowlands=true},
}
local ns={}
for _,name in ipairs({"Database.lua","MusicSCAN.lua","UI.lua"}) do
    assert(loadfile(root..name))("MusicSCAN",ns)
end
local events
for _,f in ipairs(frames) do if f.events.ADDON_LOADED then events=f;break end end
assert(events)
events.scripts.OnEvent(events,"ADDON_LOADED","MusicSCAN")
assert(ns.VERSION=="0.7.1-forever-alpha.2" and #ns.Catalog==570)
assert(ns.GetSelectedTrack().expansion=="Original World of Warcraft")
assert(not ns.State.playing and #engineCalls==0)
assert(ns.DB.favorites[936340] and ns.DB.favorites[8158670] and ns.DB.favorites[999999999])
assert(not ns.DB.favorites[-1] and not ns.DB.favorites.bad)
assert(ns.DB.window.width==640 and ns.DB.window.x==35 and ns.DB.minimap.angle==42)
assert(not ns.DB.collapsedExpansions.Shadowlands)
local ids,keys,count={},{},0
for _,track in ipairs(ns.Catalog) do
    assert(not ids[track.fileDataID] and not keys[track.key])
    ids[track.fileDataID],keys[track.key]=true,true
    assert(track.expansion=="Original World of Warcraft" or track.expansion=="World of Warcraft: Forever")
    assert(track.playbackVerified==false)
    if track.expansion=="World of Warcraft: Forever" then
        count=count+1
        assert(track.sourceFilename:lower():find("sound/music/forever/",1,true)==1)
        assert(track.key=="music-"..track.fileDataID)
    end
end
assert(count==370)
local groups=ns.GetExpansionGroups("")
assert(#groups==2 and #groups[1].tracks==200 and #groups[2].tracks==370)
assert(groups[1].name=="Original World of Warcraft" and groups[2].name=="World of Warcraft: Forever")
assert(ns.GetTrack("wod-frostfire-magnificent-desolation-h")==nil)
assert(ns.TracksByFileID[936340]==nil and ns.TracksByFileID[1477339]==nil)
assert(#ns.GetFilteredCatalog("Hyjal")>=4 and #ns.GetFilteredCatalog("Riverglades")>=5)
assert(#ns.GetFilteredCatalog("[x%") == 0)
assert(#ns.GetFavoriteTracks("")==1 and ns.GetFavoriteTracks("")[1].fileDataID==8158670)
ns.DB.collapsedExpansions={}
ns.UI:Refresh()
assert(#ns.UI.rows<50, "viewport should keep bounded row frames")
for _,track in ipairs(ns.Catalog) do ns.DB.favorites[track.fileDataID]=true end
ns.FavoriteQuery=nil
local favorites=ns.GetFavoriteTracks("")
assert(#favorites==570)
for i=2,#favorites do assert(favorites[i-1].title:lower()<=favorites[i].title:lower()) end
ns.DB.favorites={[936340]=true,[999999999]=true}
ns.FavoriteQuery=nil
assert(#ns.GetFavoriteTracks("")==0)
local selected=ns.DB.selectedTrack
ns.ResetPosition()
assert(ns.DB.selectedTrack==selected and ns.DB.favorites[936340] and ns.DB.favorites[999999999])
ns.Initialize()
assert(not ns.State.playing)
-- Dispatch real registered lifecycle events; time and the audio engine are mocked.
local function Event(name, ...)
    assert(events.events[name], "event must be registered: "..name)
    events.scripts.OnEvent(events,name,...)
end
local A,B="music-8158670","music-8158714"
local function StartA()
    ns.SelectTrack(A)
    assert(ns.Play())
end
local function Transition()
    Event("PLAYER_LEAVING_WORLD")
    Event("LOADING_SCREEN_ENABLED")
    Event("PLAYER_ENTERING_WORLD",false,false)
    Event("LOADING_SCREEN_DISABLED")
end

-- Idle, initial-login and reload events never autoplay saved selections.
local baseline=#engineCalls
Event("LOADING_SCREEN_ENABLED")
Event("PLAYER_ENTERING_WORLD",true,false)
Event("LOADING_SCREEN_DISABLED")
Advance(10)
Event("PLAYER_ENTERING_WORLD",false,true)
Event("LOADING_SCREEN_DISABLED")
Transition();Advance(10)
assert(#engineCalls==baseline and PendingTimers()==0 and not ns.State.playing)

-- A slow load must finish before the one-second delay starts. Restore active A,
-- even though the user highlighted B, and even if the player window is hidden.
StartA();ns.SelectTrack(B);ns.UI.frame:Hide()
baseline=#engineCalls
Event("PLAYER_LEAVING_WORLD");Event("LOADING_SCREEN_ENABLED")
Event("PLAYER_ENTERING_WORLD",false,false)
Advance(30)
assert(#engineCalls==baseline and PendingTimers()==0)
Event("LOADING_SCREEN_DISABLED")
assert(PendingTimers()==1)
Advance(.9);assert(#engineCalls==baseline)
Advance(.2)
assert(#engineCalls==baseline+2 and engineCalls[#engineCalls][2]==8158670)
assert(ns.State.activeTrack==A and ns.DB.selectedTrack==B and not ns.UI.frame:IsShown())
ns.UI.frame:Show();assert(ns.UI.nowTitle:GetText()=="Hyjal General A")
assert(PendingTimers()==0)
Advance(10000);assert(#engineCalls==baseline+2, "recovery must not poll or repeat")

-- Stop wins during loading, during the delay, and against an already queued callback.
Transition()
local stale=timers[#timers]
assert(ns.Stop());baseline=#engineCalls
stale.callback();Advance(2)
assert(#engineCalls==baseline and not ns.State.playing)
StartA();Event("LOADING_SCREEN_ENABLED");ns.Stop();baseline=#engineCalls
Event("PLAYER_ENTERING_WORLD",false,false);Event("LOADING_SCREEN_DISABLED");Advance(2)
assert(#engineCalls==baseline and PendingTimers()==0)

-- Explicit Play cancels restoration, including replaying the very same file.
StartA();Transition();stale=timers[#timers]
ns.SelectTrack(B);assert(ns.Play());baseline=#engineCalls
stale.callback();Advance(2)
assert(#engineCalls==baseline and ns.State.activeTrack==B)
Transition();stale=timers[#timers]
assert(ns.Play());baseline=#engineCalls
stale.callback();Advance(2)
assert(#engineCalls==baseline and ns.State.activeTrack==B)

-- Consecutive loads and reversed finish/entry ordering still restore only once.
StartA();Transition();stale=timers[#timers];baseline=#engineCalls
Event("LOADING_SCREEN_ENABLED");Advance(2)
assert(#engineCalls==baseline and PendingTimers()==0)
Event("PLAYER_LEAVING_WORLD");Event("LOADING_SCREEN_DISABLED")
assert(PendingTimers()==0)
Event("PLAYER_ENTERING_WORLD",false,false)
stale.callback();assert(PendingTimers()==1)
Event("PLAYER_ENTERING_WORLD",false,false);Event("LOADING_SCREEN_DISABLED")
assert(PendingTimers()==1)
Advance(1);assert(#engineCalls==baseline+2 and ns.State.activeTrack==A)
Event("LOADING_SCREEN_DISABLED");Advance(2)
assert(#engineCalls==baseline+2 and PendingTimers()==0)

-- Disabled audio and rejected/throwing requests clear the stale Playing display.
for _,cvar in ipairs({"Sound_EnableMusic","Sound_EnableAllSound"}) do
    StartA();Transition();baseline=#engineCalls
    cvars[cvar]=false;Advance(1)
    assert(not ns.State.playing and #engineCalls==baseline)
    assert(ns.UI.nowLabel:GetText()=="SELECTED TRACK" and not ns.UI.stop:IsEnabled())
    cvars[cvar]=true
end
StartA();Transition();musicAccepted=false;Advance(1)
assert(not ns.State.playing and ns.UI.nowLabel:GetText()=="SELECTED TRACK")
musicAccepted=true
StartA();Transition();musicThrows=true;Advance(1)
assert(not ns.State.playing)
musicThrows=false

-- Nil success returns remain accepted, matching explicit Play behavior.
StartA();Transition();musicAccepted=nil;Advance(1)
assert(ns.State.playing and ns.State.activeTrack==A)
musicAccepted=true

-- Logout and reinitialization invalidate delayed callbacks without changing favorites.
Transition();stale=timers[#timers];baseline=#engineCalls
Event("PLAYER_LOGOUT");stale.callback();Advance(2)
assert(#engineCalls==baseline and PendingTimers()==0)
ns.ToggleFavorite(A)
Transition();stale=timers[#timers]
ns.Initialize();baseline=#engineCalls
Event("PLAYER_ENTERING_WORLD",false,true);Event("LOADING_SCREEN_DISABLED")
stale.callback();Advance(2)
assert(#engineCalls==baseline and not ns.State.playing and ns.IsFavorite(A))
assert(PendingTimers()==0 and ns.UI.frame.scripts.OnUpdate==nil)
assert(not events.events.ZONE_CHANGED_NEW_AREA and not events.events.PLAYER_REGEN_DISABLED)

io.write("PASS: Forever catalog, persistence, bounded rows and full loading-recovery scenarios.\n")
