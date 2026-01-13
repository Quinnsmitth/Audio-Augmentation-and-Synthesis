from pedalboard import load_plugin

def initialize_plugin(plugin):
    plugin.parameters['hq'].value = True
    plugin.parameters['od_power'].value = True
    plugin.parameters['od_attack'].value = "A1"
    plugin.parameters['input_gain'].value = 0.0
    plugin.parameters['output_gain'].value = 0.0
    plugin.parameters['mix'].value = 100.0
    plugin.parameters['od_level'].value = 0.5
    plugin.parameters['noise_gate'].value = 0.0
    plugin.parameters['bypass'].value = False
    return plugin