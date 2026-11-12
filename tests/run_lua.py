"""Run existing WoW-frame mocks under Lua 5.1 and 5.4; requires lupa."""
import os
from pathlib import Path
from lupa.lua51 import LuaRuntime as Lua51
from lupa.lua54 import LuaRuntime as Lua54

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
test = (ROOT / 'tests/smoke.lua').read_text(encoding='utf-8')
for runtime in (Lua51, Lua54):
    for missing_monk in (False, True):
        lua = runtime()
        script = test.replace('RAID_CLASS_COLORS = {MONK={r=0,g=1,b=152/255}}',
                              'RAID_CLASS_COLORS = {}') if missing_monk else test
        lua.execute(script)
        print(lua.eval('_VERSION'), 'missing Monk:', missing_monk, 'PASS')
