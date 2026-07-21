import os
import agent.tool_dispatch_helpers as tdh
import hermes_cli.oneshot as oneshot

def register(ctx):
    # Adapt our features as non-breaking changes via plugin monkeypatching
    
    # 1. Parallel safety and untrusted marking for custom tools
    if isinstance(tdh._PARALLEL_SAFE_TOOLS, frozenset):
        tdh._PARALLEL_SAFE_TOOLS = set(tdh._PARALLEL_SAFE_TOOLS)
    if isinstance(tdh._UNTRUSTED_TOOL_NAMES, frozenset):
        tdh._UNTRUSTED_TOOL_NAMES = set(tdh._UNTRUSTED_TOOL_NAMES)
        
    tdh._PARALLEL_SAFE_TOOLS.add("council_deliberate")
    tdh._UNTRUSTED_TOOL_NAMES.add("council_deliberate")
    
    # 2. Hard exit in oneshot to prevent hanging
    original_run_oneshot = oneshot.run_oneshot
    
    def patched_run_oneshot(*args, **kwargs):
        ret = original_run_oneshot(*args, **kwargs)
        if ret in (1, 2):
            os._exit(ret)
        return ret
        
    oneshot.run_oneshot = patched_run_oneshot
