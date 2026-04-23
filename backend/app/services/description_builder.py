from app.rules.lighting_profile import LIGHTING_ETS_PROFILE


def build_lighting_description(group) -> str:
    pattern = LIGHTING_ETS_PROFILE["description"]["pattern"]
    dimmer_suffix = ""

    if getattr(group, "dimmer_channel", None):
        dimmer_suffix = LIGHTING_ETS_PROFILE["description"]["dimmer_suffix_pattern"].format(
            dimmer_channel=group.dimmer_channel
        )

    return pattern.format(
        device_type=group.device_type or "",
        device_address=group.device_address or "",
        device_output=group.device_output or "",
        dimmer_suffix=dimmer_suffix,
        load_type=group.load_type or "",
    ).strip()
