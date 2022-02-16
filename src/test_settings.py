import pico_steer.settings

settings = pico_steer.settings.Settings(debug=True)
print(settings.settings)
print('Save')
settings.settings['steerOffset'] = -12.3
settings.save_settings()
print(settings.settings)
