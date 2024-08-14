import bpy

class CC4_Material_Cache_Parameters:

    def get_cc4_head_parameters(mat_cache):
        cc4_head_params = {}

        cc4_head_params['skin_diffuse_color'] = mat_cache.parameters.skin_diffuse_color
        cc4_head_params['skin_diffuse_hue'] = mat_cache.parameters.skin_diffuse_hue
        cc4_head_params['skin_diffuse_brightness'] = mat_cache.parameters.skin_diffuse_brightness
        cc4_head_params['skin_diffuse_saturation'] = mat_cache.parameters.skin_diffuse_saturation
        cc4_head_params['skin_diffuse_hsv_strength'] = mat_cache.parameters.skin_diffuse_hsv_strength
        cc4_head_params['skin_cavity_ao_strength'] = mat_cache.parameters.skin_cavity_ao_strength
        cc4_head_params['skin_blend_overlay_strength'] = mat_cache.parameters.skin_blend_overlay_strength
        cc4_head_params['skin_ao_strength'] = mat_cache.parameters.skin_ao_strength
        cc4_head_params['skin_ao_power'] = mat_cache.parameters.skin_ao_power
        cc4_head_params['skin_mouth_ao'] = mat_cache.parameters.skin_mouth_ao
        cc4_head_params['skin_nostril_ao'] = mat_cache.parameters.skin_nostril_ao
        cc4_head_params['skin_lips_ao'] = mat_cache.parameters.skin_lips_ao
        cc4_head_params['skin_subsurface_falloff'] = mat_cache.parameters.skin_subsurface_falloff
        cc4_head_params['skin_subsurface_radius'] = mat_cache.parameters.skin_subsurface_radius
        cc4_head_params['skin_specular_scale'] = mat_cache.parameters.skin_specular_scale
        cc4_head_params['skin_roughness_power'] = mat_cache.parameters.skin_roughness_power
        cc4_head_params['skin_roughness_min'] = mat_cache.parameters.skin_roughness_min
        cc4_head_params['skin_roughness_max'] = mat_cache.parameters.skin_roughness_max
        
        cc4_head_params['skin_specular_detail_mask'] = mat_cache.parameters.skin_specular_detail_mask
        cc4_head_params['skin_specular_detail_min'] = mat_cache.parameters.skin_specular_detail_min
        cc4_head_params['skin_specular_detail_max'] = mat_cache.parameters.skin_specular_detail_max
        cc4_head_params['skin_specular_detail_power'] = mat_cache.parameters.skin_specular_detail_power
        cc4_head_params['skin_secondary_specular_scale'] = mat_cache.parameters.skin_secondary_specular_scale
        cc4_head_params['skin_secondary_roughness_power'] = mat_cache.parameters.skin_secondary_roughness_power
        cc4_head_params['skin_specular_mix'] = mat_cache.parameters.skin_specular_mix

        cc4_head_params['skin_normal_strength'] = mat_cache.parameters.skin_normal_strength
        cc4_head_params['skin_micro_normal_strength'] = mat_cache.parameters.skin_micro_normal_strength
        cc4_head_params['skin_normal_blend_strength'] = mat_cache.parameters.skin_normal_blend_strength
        cc4_head_params['skin_unmasked_scatter_scale'] = mat_cache.parameters.skin_unmasked_scatter_scale
        cc4_head_params['skin_nose_scatter_scale'] = mat_cache.parameters.skin_nose_scatter_scale
        cc4_head_params['skin_mouth_scatter_scale'] = mat_cache.parameters.skin_mouth_scatter_scale
        cc4_head_params['skin_upper_lid_scatter_scale'] = mat_cache.parameters.skin_upper_lid_scatter_scale
        cc4_head_params['skin_inner_lid_scatter_scale'] = mat_cache.parameters.skin_inner_lid_scatter_scale
        cc4_head_params['skin_cheek_scatter_scale'] = mat_cache.parameters.skin_cheek_scatter_scale
        cc4_head_params['skin_forehead_scatter_scale'] = mat_cache.parameters.skin_forehead_scatter_scale
        cc4_head_params['skin_upper_lip_scatter_scale'] = mat_cache.parameters.skin_upper_lip_scatter_scale
        cc4_head_params['skin_chin_scatter_scale'] = mat_cache.parameters.skin_chin_scatter_scale
        cc4_head_params['skin_ear_scatter_scale'] = mat_cache.parameters.skin_ear_scatter_scale
        cc4_head_params['skin_neck_scatter_scale'] = mat_cache.parameters.skin_neck_scatter_scale
        cc4_head_params['skin_subsurface_scale'] = mat_cache.parameters.skin_subsurface_scale
        cc4_head_params['skin_micro_roughness_mod'] = mat_cache.parameters.skin_micro_roughness_mod
        cc4_head_params['skin_unmasked_roughness_mod'] = mat_cache.parameters.skin_unmasked_roughness_mod
        cc4_head_params['skin_nose_roughness_mod'] = mat_cache.parameters.skin_nose_roughness_mod
        cc4_head_params['skin_mouth_roughness_mod'] = mat_cache.parameters.skin_mouth_roughness_mod
        cc4_head_params['skin_upper_lid_roughness_mod'] = mat_cache.parameters.skin_upper_lid_roughness_mod
        cc4_head_params['skin_inner_lid_roughness_mod'] = mat_cache.parameters.skin_inner_lid_roughness_mod
        cc4_head_params['skin_cheek_roughness_mod'] = mat_cache.parameters.skin_cheek_roughness_mod
        cc4_head_params['skin_forehead_roughness_mod'] = mat_cache.parameters.skin_forehead_roughness_mod
        cc4_head_params['skin_upper_lip_roughness_mod'] = mat_cache.parameters.skin_upper_lip_roughness_mod
        cc4_head_params['skin_chin_roughness_mod'] = mat_cache.parameters.skin_chin_roughness_mod
        cc4_head_params['skin_ear_roughness_mod'] = mat_cache.parameters.skin_ear_roughness_mod
        cc4_head_params['skin_neck_roughness_mod'] = mat_cache.parameters.skin_neck_roughness_mod
        cc4_head_params['skin_emissive_color'] = mat_cache.parameters.skin_emissive_color
        cc4_head_params['skin_emission_strength'] = mat_cache.parameters.skin_emission_strength
        cc4_head_params['skin_micro_normal_tiling'] = mat_cache.parameters.skin_micro_normal_tiling
        cc4_head_params['skin_height_scale'] = mat_cache.parameters.skin_height_scale
        cc4_head_params['skin_height_delta_scale'] = mat_cache.parameters.skin_height_delta_scale

        return cc4_head_params

    def get_cc4_skin_parameters(mat_cache):
        cc4_skin_params = {}

        cc4_skin_params['skin_diffuse_color'] = mat_cache.parameters.skin_diffuse_color
        cc4_skin_params['skin_diffuse_hue'] = mat_cache.parameters.skin_diffuse_hue
        cc4_skin_params['skin_diffuse_brightness'] = mat_cache.parameters.skin_diffuse_brightness
        cc4_skin_params['skin_diffuse_saturation'] = mat_cache.parameters.skin_diffuse_saturation
        cc4_skin_params['skin_diffuse_hsv_strength'] = mat_cache.parameters.skin_diffuse_hsv_strength
        cc4_skin_params['skin_ao_strength'] = mat_cache.parameters.skin_ao_strength
        cc4_skin_params['skin_ao_power'] = mat_cache.parameters.skin_ao_power
        cc4_skin_params['skin_subsurface_falloff'] = mat_cache.parameters.skin_subsurface_falloff
        cc4_skin_params['skin_subsurface_radius'] = mat_cache.parameters.skin_subsurface_radius
        cc4_skin_params['skin_specular_scale'] = mat_cache.parameters.skin_specular_scale
        cc4_skin_params['skin_roughness_power'] = mat_cache.parameters.skin_roughness_power
        cc4_skin_params['skin_roughness_min'] = mat_cache.parameters.skin_roughness_min
        cc4_skin_params['skin_roughness_max'] = mat_cache.parameters.skin_roughness_max
        
        cc4_skin_params['skin_specular_detail_mask'] = mat_cache.parameters.skin_specular_detail_mask
        cc4_skin_params['skin_specular_detail_min'] = mat_cache.parameters.skin_specular_detail_min
        cc4_skin_params['skin_specular_detail_max'] = mat_cache.parameters.skin_specular_detail_max
        cc4_skin_params['skin_specular_detail_power'] = mat_cache.parameters.skin_specular_detail_power
        cc4_skin_params['skin_secondary_specular_scale'] = mat_cache.parameters.skin_secondary_specular_scale
        cc4_skin_params['skin_secondary_roughness_power'] = mat_cache.parameters.skin_secondary_roughness_power
        cc4_skin_params['skin_specular_mix'] = mat_cache.parameters.skin_specular_mix

        cc4_skin_params['skin_normal_strength'] = mat_cache.parameters.skin_normal_strength
        cc4_skin_params['skin_micro_normal_strength'] = mat_cache.parameters.skin_micro_normal_strength
        cc4_skin_params['skin_unmasked_scatter_scale'] = mat_cache.parameters.skin_unmasked_scatter_scale
        cc4_skin_params['skin_r_scatter_scale'] = mat_cache.parameters.skin_r_scatter_scale
        cc4_skin_params['skin_g_scatter_scale'] = mat_cache.parameters.skin_g_scatter_scale
        cc4_skin_params['skin_b_scatter_scale'] = mat_cache.parameters.skin_b_scatter_scale
        cc4_skin_params['skin_a_scatter_scale'] = mat_cache.parameters.skin_a_scatter_scale
        cc4_skin_params['skin_micro_roughness_mod'] = mat_cache.parameters.skin_micro_roughness_mod
        cc4_skin_params['skin_unmasked_roughness_mod'] = mat_cache.parameters.skin_unmasked_roughness_mod
        cc4_skin_params['skin_r_roughness_mod'] = mat_cache.parameters.skin_r_roughness_mod
        cc4_skin_params['skin_g_roughness_mod'] = mat_cache.parameters.skin_g_roughness_mod
        cc4_skin_params['skin_b_roughness_mod'] = mat_cache.parameters.skin_b_roughness_mod
        cc4_skin_params['skin_a_roughness_mod'] = mat_cache.parameters.skin_a_roughness_mod
        cc4_skin_params['skin_emissive_color'] = mat_cache.parameters.skin_emissive_color
        cc4_skin_params['skin_emission_strength'] = mat_cache.parameters.skin_emission_strength
        cc4_skin_params['skin_micro_normal_tiling'] = mat_cache.parameters.skin_micro_normal_tiling

        return cc4_skin_params

    def get_cc4_eye_parameters(mat_cache):
        cc4_eye_params = {}

        cc4_eye_params['eye_subsurface_scale'] = mat_cache.parameters.eye_subsurface_scale
        cc4_eye_params['eye_subsurface_radius'] = mat_cache.parameters.eye_subsurface_radius
        cc4_eye_params['eye_subsurface_falloff'] = mat_cache.parameters.eye_subsurface_falloff
        cc4_eye_params['eye_cornea_specular'] = mat_cache.parameters.eye_cornea_specular
        cc4_eye_params['eye_iris_specular'] = mat_cache.parameters.eye_iris_specular
        cc4_eye_params['eye_sclera_roughness'] = mat_cache.parameters.eye_sclera_roughness
        cc4_eye_params['eye_iris_roughness'] = mat_cache.parameters.eye_iris_roughness
        cc4_eye_params['eye_cornea_roughness'] = mat_cache.parameters.eye_cornea_roughness
        cc4_eye_params['eye_ao_strength'] = mat_cache.parameters.eye_ao_strength
        cc4_eye_params['eye_sclera_scale'] = mat_cache.parameters.eye_sclera_scale
        cc4_eye_params['eye_sclera_hue'] = mat_cache.parameters.eye_sclera_hue
        cc4_eye_params['eye_sclera_saturation'] = mat_cache.parameters.eye_sclera_saturation
        cc4_eye_params['eye_sclera_brightness'] = mat_cache.parameters.eye_sclera_brightness
        cc4_eye_params['eye_sclera_hsv'] = mat_cache.parameters.eye_sclera_hsv
        cc4_eye_params['eye_iris_scale'] = mat_cache.parameters.eye_iris_scale
        cc4_eye_params['eye_iris_hue'] = mat_cache.parameters.eye_iris_hue
        cc4_eye_params['eye_iris_saturation'] = mat_cache.parameters.eye_iris_saturation
        cc4_eye_params['eye_iris_brightness'] = mat_cache.parameters.eye_iris_brightness
        cc4_eye_params['eye_iris_hsv'] = mat_cache.parameters.eye_iris_hsv
        cc4_eye_params['eye_iris_radius'] = mat_cache.parameters.eye_iris_radius
        cc4_eye_params['eye_iris_color'] = mat_cache.parameters.eye_iris_color
        cc4_eye_params['eye_iris_inner_color'] = mat_cache.parameters.eye_iris_inner_color
        cc4_eye_params['eye_iris_cloudy_color'] = mat_cache.parameters.eye_iris_cloudy_color
        cc4_eye_params['eye_iris_inner_scale'] = mat_cache.parameters.eye_iris_inner_scale
        cc4_eye_params['eye_limbus_width'] = mat_cache.parameters.eye_limbus_width
        cc4_eye_params['eye_limbus_dark_radius'] = mat_cache.parameters.eye_limbus_dark_radius
        cc4_eye_params['eye_limbus_dark_width'] = mat_cache.parameters.eye_limbus_dark_width
        cc4_eye_params['eye_limbus_color'] = mat_cache.parameters.eye_limbus_color
        cc4_eye_params['eye_shadow_radius'] = mat_cache.parameters.eye_shadow_radius
        cc4_eye_params['eye_shadow_hardness'] = mat_cache.parameters.eye_shadow_hardness
        cc4_eye_params['eye_corner_shadow_color'] = mat_cache.parameters.eye_corner_shadow_color
        cc4_eye_params['eye_color_blend_strength'] = mat_cache.parameters.eye_color_blend_strength
        cc4_eye_params['eye_sclera_emissive_color'] = mat_cache.parameters.eye_sclera_emissive_color
        cc4_eye_params['eye_sclera_emission_strength'] = mat_cache.parameters.eye_sclera_emission_strength
        cc4_eye_params['eye_iris_emissive_color'] = mat_cache.parameters.eye_iris_emissive_color
        cc4_eye_params['eye_iris_emission_strength'] = mat_cache.parameters.eye_iris_emission_strength
        cc4_eye_params['eye_sclera_normal_strength'] = mat_cache.parameters.eye_sclera_normal_strength
        cc4_eye_params['eye_sclera_normal_tiling'] = mat_cache.parameters.eye_sclera_normal_tiling
        cc4_eye_params['eye_refraction_depth'] = mat_cache.parameters.eye_refraction_depth
        cc4_eye_params['eye_ior'] = mat_cache.parameters.eye_ior
        cc4_eye_params['eye_blood_vessel_height'] = mat_cache.parameters.eye_blood_vessel_height
        cc4_eye_params['eye_iris_bump_height'] = mat_cache.parameters.eye_iris_bump_height
        cc4_eye_params['eye_iris_depth'] = mat_cache.parameters.eye_iris_depth
        cc4_eye_params['eye_iris_depth_radius'] = mat_cache.parameters.eye_iris_depth_radius
        cc4_eye_params['eye_pupil_scale'] = mat_cache.parameters.eye_pupil_scale

        return cc4_eye_params

    def get_cc4_tearline_parameters(mat_cache):
        cc4_tearline_params = {}

        cc4_tearline_params['tearline_specular'] = mat_cache.parameters.tearline_specular
        cc4_tearline_params['tearline_glossiness'] = mat_cache.parameters.tearline_glossiness
        cc4_tearline_params['tearline_alpha'] = mat_cache.parameters.tearline_alpha
        cc4_tearline_params['tearline_roughness'] = mat_cache.parameters.tearline_roughness
        cc4_tearline_params['tearline_inner'] = mat_cache.parameters.tearline_inner
        cc4_tearline_params['tearline_displace'] = mat_cache.parameters.tearline_displace

        return cc4_tearline_params

    def get_cc4_tongue_parameters(mat_cache):
        cc4_tougue_params = {}

        cc4_tougue_params['tongue_hue'] = mat_cache.parameters.tongue_hue
        cc4_tougue_params['tongue_brightness'] = mat_cache.parameters.tongue_brightness
        cc4_tougue_params['tongue_saturation'] = mat_cache.parameters.tongue_saturation
        cc4_tougue_params['tongue_hsv_strength'] = mat_cache.parameters.tongue_hsv_strength
        cc4_tougue_params['tongue_front_ao'] = mat_cache.parameters.tongue_front_ao
        cc4_tougue_params['tongue_rear_ao'] = mat_cache.parameters.tongue_rear_ao
        cc4_tougue_params['tongue_ao_strength'] = mat_cache.parameters.tongue_ao_strength
        cc4_tougue_params['tongue_ao_power'] = mat_cache.parameters.tongue_ao_power
        cc4_tougue_params['tongue_subsurface_scatter'] = mat_cache.parameters.tongue_subsurface_scatter
        cc4_tougue_params['tongue_subsurface_radius'] = mat_cache.parameters.tongue_subsurface_radius
        cc4_tougue_params['tongue_subsurface_falloff'] = mat_cache.parameters.tongue_subsurface_falloff
        cc4_tougue_params['tongue_front_specular'] = mat_cache.parameters.tongue_front_specular
        cc4_tougue_params['tongue_rear_specular'] = mat_cache.parameters.tongue_rear_specular
        cc4_tougue_params['tongue_front_roughness'] = mat_cache.parameters.tongue_front_roughness
        cc4_tougue_params['tongue_rear_roughness'] = mat_cache.parameters.tongue_rear_roughness
        cc4_tougue_params['tongue_normal_strength'] = mat_cache.parameters.tongue_normal_strength
        cc4_tougue_params['tongue_micro_normal_strength'] = mat_cache.parameters.tongue_micro_normal_strength
        cc4_tougue_params['tongue_micro_normal_tiling'] = mat_cache.parameters.tongue_micro_normal_tiling
        cc4_tougue_params['tongue_emissive_color'] = mat_cache.parameters.tongue_emissive_color
        cc4_tougue_params['tongue_emission_strength'] = mat_cache.parameters.tongue_emission_strength

        return cc4_tougue_params

    def get_cc4_eye_occlusion_parameters(mat_cache):
        cc4_eye_occlusion_params = {}

        cc4_eye_occlusion_params['eye_occlusion'] = mat_cache.parameters.eye_occlusion
        cc4_eye_occlusion_params['eye_occlusion_color'] = mat_cache.parameters.eye_occlusion_color
        cc4_eye_occlusion_params['eye_occlusion_hardness'] = mat_cache.parameters.eye_occlusion_hardness
        cc4_eye_occlusion_params['eye_occlusion_strength'] = mat_cache.parameters.eye_occlusion_strength
        cc4_eye_occlusion_params['eye_occlusion_power'] = mat_cache.parameters.eye_occlusion_power
        cc4_eye_occlusion_params['eye_occlusion_top_min'] = mat_cache.parameters.eye_occlusion_top_min
        cc4_eye_occlusion_params['eye_occlusion_top_range'] = mat_cache.parameters.eye_occlusion_top_range
        cc4_eye_occlusion_params['eye_occlusion_top_curve'] = mat_cache.parameters.eye_occlusion_top_curve
        cc4_eye_occlusion_params['eye_occlusion_bottom_min'] = mat_cache.parameters.eye_occlusion_bottom_min
        cc4_eye_occlusion_params['eye_occlusion_bottom_range'] = mat_cache.parameters.eye_occlusion_bottom_range
        cc4_eye_occlusion_params['eye_occlusion_bottom_curve'] = mat_cache.parameters.eye_occlusion_bottom_curve
        cc4_eye_occlusion_params['eye_occlusion_inner_min'] = mat_cache.parameters.eye_occlusion_inner_min
        cc4_eye_occlusion_params['eye_occlusion_inner_range'] = mat_cache.parameters.eye_occlusion_inner_range
        cc4_eye_occlusion_params['eye_occlusion_outer_min'] = mat_cache.parameters.eye_occlusion_outer_min
        cc4_eye_occlusion_params['eye_occlusion_outer_range'] = mat_cache.parameters.eye_occlusion_outer_range
        cc4_eye_occlusion_params['eye_occlusion_strength2'] = mat_cache.parameters.eye_occlusion_strength2
        cc4_eye_occlusion_params['eye_occlusion_top2_min'] = mat_cache.parameters.eye_occlusion_top2_min
        cc4_eye_occlusion_params['eye_occlusion_top2_range'] = mat_cache.parameters.eye_occlusion_top2_range
        cc4_eye_occlusion_params['eye_occlusion_tear_duct_position'] = mat_cache.parameters.eye_occlusion_tear_duct_position
        cc4_eye_occlusion_params['eye_occlusion_tear_duct_width'] = mat_cache.parameters.eye_occlusion_tear_duct_width
        cc4_eye_occlusion_params['eye_occlusion_inner'] = mat_cache.parameters.eye_occlusion_inner
        cc4_eye_occlusion_params['eye_occlusion_outer'] = mat_cache.parameters.eye_occlusion_outer
        cc4_eye_occlusion_params['eye_occlusion_top'] = mat_cache.parameters.eye_occlusion_top
        cc4_eye_occlusion_params['eye_occlusion_bottom'] = mat_cache.parameters.eye_occlusion_bottom
        cc4_eye_occlusion_params['eye_occlusion_displace'] = mat_cache.parameters.eye_occlusion_displace

        return cc4_eye_occlusion_params

    def get_cc4_hair_parameters(mat_cache):
        cc4_hair_params = {}

        cc4_hair_params['hair_diffuse_color'] = mat_cache.parameters.hair_diffuse_color
        cc4_hair_params['hair_diffuse_hue'] = mat_cache.parameters.hair_diffuse_hue
        cc4_hair_params['hair_diffuse_brightness'] = mat_cache.parameters.hair_diffuse_brightness
        cc4_hair_params['hair_diffuse_saturation'] = mat_cache.parameters.hair_diffuse_saturation
        cc4_hair_params['hair_diffuse_hsv_strength'] = mat_cache.parameters.hair_diffuse_hsv_strength
        cc4_hair_params['hair_global_strength'] = mat_cache.parameters.hair_global_strength
        cc4_hair_params['hair_root_color_strength'] = mat_cache.parameters.hair_root_color_strength
        cc4_hair_params['hair_end_color_strength'] = mat_cache.parameters.hair_end_color_strength
        cc4_hair_params['hair_invert_root_map'] = mat_cache.parameters.hair_invert_root_map
        cc4_hair_params['hair_base_color_strength'] = mat_cache.parameters.hair_base_color_strength
        cc4_hair_params['hair_root_color'] = mat_cache.parameters.hair_root_color
        cc4_hair_params['hair_end_color'] = mat_cache.parameters.hair_end_color
        cc4_hair_params['hair_highlight_a_color'] = mat_cache.parameters.hair_highlight_a_color
        cc4_hair_params['hair_highlight_a_start'] = mat_cache.parameters.hair_highlight_a_start
        cc4_hair_params['hair_highlight_a_mid'] = mat_cache.parameters.hair_highlight_a_mid
        cc4_hair_params['hair_highlight_a_end'] = mat_cache.parameters.hair_highlight_a_end
        cc4_hair_params['hair_highlight_a_strength'] = mat_cache.parameters.hair_highlight_a_strength
        cc4_hair_params['hair_highlight_a_overlap_invert'] = mat_cache.parameters.hair_highlight_a_overlap_invert
        cc4_hair_params['hair_highlight_a_overlap_end'] = mat_cache.parameters.hair_highlight_a_overlap_end
        cc4_hair_params['hair_highlight_b_color'] = mat_cache.parameters.hair_highlight_b_color
        cc4_hair_params['hair_highlight_b_start'] = mat_cache.parameters.hair_highlight_b_start
        cc4_hair_params['hair_highlight_b_mid'] = mat_cache.parameters.hair_highlight_b_mid
        cc4_hair_params['hair_highlight_b_end'] = mat_cache.parameters.hair_highlight_b_end
        cc4_hair_params['hair_highlight_b_strength'] = mat_cache.parameters.hair_highlight_b_strength
        cc4_hair_params['hair_highlight_b_overlap_invert'] = mat_cache.parameters.hair_highlight_b_overlap_invert
        cc4_hair_params['hair_highlight_b_overlap_end'] = mat_cache.parameters.hair_highlight_b_overlap_end
        cc4_hair_params['hair_vertex_color_strength'] = mat_cache.parameters.hair_vertex_color_strength
        cc4_hair_params['hair_vertex_color'] = mat_cache.parameters.hair_vertex_color
        cc4_hair_params['hair_anisotropic_roughness'] = mat_cache.parameters.hair_anisotropic_roughness
        cc4_hair_params['hair_anisotropic_shift_min'] = mat_cache.parameters.hair_anisotropic_shift_min
        cc4_hair_params['hair_anisotropic_shift_max'] = mat_cache.parameters.hair_anisotropic_shift_max
        cc4_hair_params['hair_anisotropic'] = mat_cache.parameters.hair_anisotropic
        cc4_hair_params['hair_anisotropic_strength'] = mat_cache.parameters.hair_anisotropic_strength
        cc4_hair_params['hair_specular_blend'] = mat_cache.parameters.hair_specular_blend
        cc4_hair_params['hair_anisotropic_strength2'] = mat_cache.parameters.hair_anisotropic_strength2
        cc4_hair_params['hair_anisotropic_strength_cycles'] = mat_cache.parameters.hair_anisotropic_strength_cycles
        cc4_hair_params['hair_anisotropic_color'] = mat_cache.parameters.hair_anisotropic_color
        cc4_hair_params['hair_subsurface_scale'] = mat_cache.parameters.hair_subsurface_scale
        cc4_hair_params['hair_subsurface_falloff'] = mat_cache.parameters.hair_subsurface_falloff
        cc4_hair_params['hair_subsurface_radius'] = mat_cache.parameters.hair_subsurface_radius
        cc4_hair_params['hair_diffuse_strength'] = mat_cache.parameters.hair_diffuse_strength
        cc4_hair_params['hair_ao_strength'] = mat_cache.parameters.hair_ao_strength
        cc4_hair_params['hair_ao_power'] = mat_cache.parameters.hair_ao_power
        cc4_hair_params['hair_ao_occlude_all'] = mat_cache.parameters.hair_ao_occlude_all
        cc4_hair_params['hair_blend_multiply_strength'] = mat_cache.parameters.hair_blend_multiply_strength
        cc4_hair_params['hair_specular_scale'] = mat_cache.parameters.hair_specular_scale
        cc4_hair_params['hair_roughness_strength'] = mat_cache.parameters.hair_roughness_strength
        cc4_hair_params['hair_alpha_strength'] = mat_cache.parameters.hair_alpha_strength
        cc4_hair_params['hair_opacity'] = mat_cache.parameters.hair_opacity
        cc4_hair_params['hair_normal_strength'] = mat_cache.parameters.hair_normal_strength
        cc4_hair_params['hair_bump_strength'] = mat_cache.parameters.hair_bump_strength
        cc4_hair_params['hair_displacement_strength'] = mat_cache.parameters.hair_displacement_strength
        cc4_hair_params['hair_emissive_color'] = mat_cache.parameters.hair_emissive_color
        cc4_hair_params['hair_emission_strength'] = mat_cache.parameters.hair_emission_strength
        cc4_hair_params['hair_enable_color'] = mat_cache.parameters.hair_enable_color
        cc4_hair_params['hair_tangent_vector'] = mat_cache.parameters.hair_tangent_vector
        cc4_hair_params['hair_tangent_flip_green'] = mat_cache.parameters.hair_tangent_flip_green
        cc4_hair_params['hair_specular_scale2'] = mat_cache.parameters.hair_specular_scale2

        return cc4_hair_params

    def get_cc4_teeth_parameters(mat_cache):
        cc4_teeth_params = {}

        cc4_teeth_params['teeth_gums_hue'] = mat_cache.parameters.teeth_gums_hue
        cc4_teeth_params['teeth_gums_brightness'] = mat_cache.parameters.teeth_gums_brightness
        cc4_teeth_params['teeth_gums_saturation'] = mat_cache.parameters.teeth_gums_saturation
        cc4_teeth_params['teeth_gums_hsv_strength'] = mat_cache.parameters.teeth_gums_hsv_strength
        cc4_teeth_params['teeth_teeth_hue'] = mat_cache.parameters.teeth_teeth_hue
        cc4_teeth_params['teeth_teeth_brightness'] = mat_cache.parameters.teeth_teeth_brightness
        cc4_teeth_params['teeth_teeth_saturation'] = mat_cache.parameters.teeth_teeth_saturation
        cc4_teeth_params['teeth_teeth_hsv_strength'] = mat_cache.parameters.teeth_teeth_hsv_strength
        cc4_teeth_params['teeth_front_ao'] = mat_cache.parameters.teeth_front_ao
        cc4_teeth_params['teeth_rear_ao'] = mat_cache.parameters.teeth_rear_ao
        cc4_teeth_params['teeth_ao_strength'] = mat_cache.parameters.teeth_ao_strength
        cc4_teeth_params['teeth_ao_power'] = mat_cache.parameters.teeth_ao_power
        cc4_teeth_params['teeth_gums_subsurface_scatter'] = mat_cache.parameters.teeth_gums_subsurface_scatter
        cc4_teeth_params['teeth_teeth_subsurface_scatter'] = mat_cache.parameters.teeth_teeth_subsurface_scatter
        cc4_teeth_params['teeth_subsurface_radius'] = mat_cache.parameters.teeth_subsurface_radius
        cc4_teeth_params['teeth_subsurface_falloff'] = mat_cache.parameters.teeth_subsurface_falloff
        cc4_teeth_params['teeth_front_specular'] = mat_cache.parameters.teeth_front_specular
        cc4_teeth_params['teeth_rear_specular'] = mat_cache.parameters.teeth_rear_specular
        cc4_teeth_params['teeth_front_roughness'] = mat_cache.parameters.teeth_front_roughness
        cc4_teeth_params['teeth_rear_roughness'] = mat_cache.parameters.teeth_rear_roughness
        cc4_teeth_params['teeth_normal_strength'] = mat_cache.parameters.teeth_normal_strength
        cc4_teeth_params['teeth_micro_normal_strength'] = mat_cache.parameters.teeth_micro_normal_strength
        cc4_teeth_params['teeth_micro_normal_tiling'] = mat_cache.parameters.teeth_micro_normal_tiling
        cc4_teeth_params['teeth_emissive_color'] = mat_cache.parameters.teeth_emissive_color
        cc4_teeth_params['teeth_emission_strength'] = mat_cache.parameters.teeth_emission_strength

        return cc4_teeth_params

    def get_cc4_pbr_parameters(mat_cache):
        cc4_pbr_params = {}

        cc4_pbr_params['default_diffuse_color'] = mat_cache.parameters.default_diffuse_color
        cc4_pbr_params['default_ao_strength'] = mat_cache.parameters.default_ao_strength
        cc4_pbr_params['default_ao_power'] = mat_cache.parameters.default_ao_power
        cc4_pbr_params['default_blend_multiply_strength'] = mat_cache.parameters.default_blend_multiply_strength
        cc4_pbr_params['default_metallic'] = mat_cache.parameters.default_metallic
        cc4_pbr_params['default_specular'] = mat_cache.parameters.default_specular
        cc4_pbr_params['default_roughness'] = mat_cache.parameters.default_roughness
        cc4_pbr_params['default_specular_strength'] = mat_cache.parameters.default_specular_strength
        cc4_pbr_params['default_specular_scale'] = mat_cache.parameters.default_specular_scale
        cc4_pbr_params['default_specular_mask'] = mat_cache.parameters.default_specular_mask
        cc4_pbr_params['default_roughness_power'] = mat_cache.parameters.default_roughness_power
        cc4_pbr_params['default_roughness_min'] = mat_cache.parameters.default_roughness_min
        cc4_pbr_params['default_roughness_max'] = mat_cache.parameters.default_roughness_max
        cc4_pbr_params['default_alpha_strength'] = mat_cache.parameters.default_alpha_strength
        cc4_pbr_params['default_opacity'] = mat_cache.parameters.default_opacity
        cc4_pbr_params['default_normal_strength'] = mat_cache.parameters.default_normal_strength
        cc4_pbr_params['default_bump_strength'] = mat_cache.parameters.default_bump_strength
        cc4_pbr_params['default_displacement_strength'] = mat_cache.parameters.default_displacement_strength
        cc4_pbr_params['default_displacement_base'] = mat_cache.parameters.default_displacement_base
        cc4_pbr_params['default_emissive_color'] = mat_cache.parameters.default_emissive_color
        cc4_pbr_params['default_emission_strength'] = mat_cache.parameters.default_emission_strength

        return cc4_pbr_params

    def get_cc4_sss_parameters(mat_cache):
        cc4_sss_params = {}

        cc4_sss_params['default_diffuse_color'] = mat_cache.parameters.default_diffuse_color
        cc4_sss_params['default_hue'] = mat_cache.parameters.default_hue
        cc4_sss_params['default_brightness'] = mat_cache.parameters.default_brightness
        cc4_sss_params['default_saturation'] = mat_cache.parameters.default_saturation
        cc4_sss_params['default_hsv_strength'] = mat_cache.parameters.default_hsv_strength
        cc4_sss_params['default_ao_strength'] = mat_cache.parameters.default_ao_strength
        cc4_sss_params['default_ao_power'] = mat_cache.parameters.default_ao_power
        cc4_sss_params['default_blend_multiply_strength'] = mat_cache.parameters.default_blend_multiply_strength
        cc4_sss_params['default_metallic'] = mat_cache.parameters.default_metallic
        cc4_sss_params['default_specular'] = mat_cache.parameters.default_specular
        cc4_sss_params['default_roughness'] = mat_cache.parameters.default_roughness
        cc4_sss_params['default_specular_strength'] = mat_cache.parameters.default_specular_strength
        cc4_sss_params['default_specular_scale'] = mat_cache.parameters.default_specular_scale
        cc4_sss_params['default_specular_mask'] = mat_cache.parameters.default_specular_mask
        cc4_sss_params['default_roughness_power'] = mat_cache.parameters.default_roughness_power
        cc4_sss_params['default_roughness_min'] = mat_cache.parameters.default_roughness_min
        cc4_sss_params['default_roughness_max'] = mat_cache.parameters.default_roughness_max
        cc4_sss_params['default_alpha_strength'] = mat_cache.parameters.default_alpha_strength
        cc4_sss_params['default_opacity'] = mat_cache.parameters.default_opacity
        cc4_sss_params['default_normal_strength'] = mat_cache.parameters.default_normal_strength
        cc4_sss_params['default_bump_strength'] = mat_cache.parameters.default_bump_strength
        cc4_sss_params['default_displacement_strength'] = mat_cache.parameters.default_displacement_strength
        cc4_sss_params['default_displacement_base'] = mat_cache.parameters.default_displacement_base
        cc4_sss_params['default_emissive_color'] = mat_cache.parameters.default_emissive_color
        cc4_sss_params['default_emission_strength'] = mat_cache.parameters.default_emission_strength
        cc4_sss_params['default_subsurface_falloff'] = mat_cache.parameters.default_subsurface_falloff
        cc4_sss_params['default_subsurface_radius'] = mat_cache.parameters.default_subsurface_radius
        cc4_sss_params['default_micro_normal_strength'] = mat_cache.parameters.default_micro_normal_strength
        cc4_sss_params['default_subsurface_scale'] = mat_cache.parameters.default_subsurface_scale
        cc4_sss_params['default_unmasked_scatter_scale'] = mat_cache.parameters.default_unmasked_scatter_scale
        cc4_sss_params['default_r_scatter_scale'] = mat_cache.parameters.default_r_scatter_scale
        cc4_sss_params['default_g_scatter_scale'] = mat_cache.parameters.default_g_scatter_scale
        cc4_sss_params['default_b_scatter_scale'] = mat_cache.parameters.default_b_scatter_scale
        cc4_sss_params['default_a_scatter_scale'] = mat_cache.parameters.default_a_scatter_scale
        cc4_sss_params['default_micro_roughness_mod'] = mat_cache.parameters.default_micro_roughness_mod
        cc4_sss_params['default_unmasked_roughness_mod'] = mat_cache.parameters.default_unmasked_roughness_mod
        cc4_sss_params['default_r_roughness_mod'] = mat_cache.parameters.default_r_roughness_mod
        cc4_sss_params['default_g_roughness_mod'] = mat_cache.parameters.default_g_roughness_mod
        cc4_sss_params['default_b_roughness_mod'] = mat_cache.parameters.default_b_roughness_mod
        cc4_sss_params['default_a_roughness_mod'] = mat_cache.parameters.default_a_roughness_mod
        cc4_sss_params['default_micro_normal_tiling'] = mat_cache.parameters.default_micro_normal_tiling

        return cc4_sss_params