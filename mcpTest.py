import EasyMCP2221

mcp = EasyMCP2221.Device()
print(f"mcp: {mcp}")
mcp.set_pin_function(gp1='ADC', gp2="ADC")
mcp.ADC_config(ref="VDD")
values = mcp.ADC_read()
print(values)