import bpy

class CHAOS_OT_CC_Blender_Processor:

    opertating_shape_key_name = 'added_shape_key_aaaa'
    cc_facial_bone_name = 'CC_Base_FacialBone'
    cc_new_facial_skeleton_name = 'Armature_Head'
    biped_head_attach_bone_name = 'Bip001 Head'

    ##############################################################################
    #-----------------------utility function -------------------
    def get_armature_object_collection(self,armature_name):
        for obj in  bpy.data.objects:
            if obj.data.name == armature_name:
                return obj
        return None

    #################################################################################
    # ------------------- Reset RestPose ----------------------------------------
    def set_animation_to_last_frame(self):
        print('1. set animation to last frame')
        # Set the current frame to the last frame
        bpy.context.scene.frame_set(bpy.context.scene.frame_end)
        # Update the scene to reflect the change
        bpy.context.view_layer.update()


    def generate_skeleton_to_shape_key(self,collection_object):
        print('2. generate skeleton to shape key')
        
        print('In collection object:',collection_object)
        # for "RuntimeError: Operator bpy.ops.object.mode_set.poll() Context missing active object"
        collection_object.select_set(True)
        bpy.context.view_layer.objects.active = collection_object
        
        # Iterate through all objects in the scene
        for obj in collection_object.children_recursive:
            if obj.type == 'MESH':
                print('in object',obj.name)
                # Check if the object has an armature modifier
                for mod in obj.modifiers:
                    print('  in modifier object',mod.object.name)
                    if (mod.type == 'ARMATURE'):
                        bpy.ops.object.select_all(action='DESELECT')
                        #bpy.context.view_layer.objects.active = mod.object
                        obj.select_set(True)
                        bpy.context.view_layer.objects.active = obj
                        bpy.ops.object.mode_set(mode='OBJECT')
                        print('    modifier_apply_as_shapekey:modifier name :', mod.name)
                        bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=False, modifier=mod.name)
                        obj.select_set(False)
                    else:
                        print('    Failed! mode type',mod.type)
                    
    def apply_skeleton_shape_key(self,collection_object):
        print('3. apply skeleton shape key and delete last shape key')
        
        print('In collection object:',collection_object)
        
        # Iterate through all objects in the scene
        for obj in collection_object.children_recursive:
            if obj.type == 'MESH':
                # Check if the object has an armature modifier
                now_operating_obj = obj
                print('in object',now_operating_obj.name)
                
                now_operating_obj.select_set(True)
                try:
                    now_operating_obj.data.shape_keys.key_blocks[-1].name = self.opertating_shape_key_name
                except AttributeError:
                    print('!!!attribute error')
                    continue
                
                print('last shape key name', now_operating_obj.data.shape_keys.key_blocks[-1].name)
                shape_idx = now_operating_obj.data.shape_keys.key_blocks.find(self.opertating_shape_key_name)
                if shape_idx > 0 :
                    bpy.ops.object.select_all(action='DESELECT')
                    now_operating_obj.select_set(True)
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.context.view_layer.objects.active = now_operating_obj
                    
                    bpy.ops.object.mode_set(mode='EDIT')
                    # Call the select_all operator
                    bpy.ops.mesh.select_all(action='SELECT')
                    print('  blend from shape:', self.opertating_shape_key_name, ' and shape index:' ,shape_idx)  
                    bpy.ops.mesh.blend_from_shape(shape=self.opertating_shape_key_name, blend=1)
                    bpy.ops.object.mode_set(mode='OBJECT')
                    
                    now_operating_obj.select_set(False)
                else:
                    print('  not fount shape key:', self.opertating_shape_key_name, 'in object:' ,obj.name)   
        
                                
        print('exiting edit mode')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        
        print('delete last shape key')
        for obj in collection_object.children_recursive:
            if obj.type == 'MESH':
                selected_obj = obj
        
                # 获取物体的形态键列表
                try:
                    shape_keys = selected_obj.data.shape_keys.key_blocks
                except AttributeError:
                    print('!!!attribute error')
                    continue
                
                
                # 获取最大的形态键数量
                max_shape_key_count = len(shape_keys)
                selected_obj.active_shape_key_index = max_shape_key_count - 1
                
                bpy.ops.object.select_all(action='DESELECT')
                selected_obj.select_set(True)
                bpy.context.view_layer.objects.active = selected_obj
                bpy.ops.object.shape_key_remove(all=False)
                selected_obj.select_set(False)
        

    def apply_skeleton_to_restpose(self,skeleton_name):
        print('4. apply skeleton to rest pose')

        for obj in bpy.context.scene.objects: 
            if obj.type == 'ARMATURE' and obj.name == skeleton_name:
                print('select target object:', skeleton_name)
                obj.select_set(True)
                
        armature = bpy.data.objects['Armature']
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature   
            
        print('entering pose mode')
        bpy.ops.object.mode_set(mode='POSE')
        print('apply pose as rest pose')
        bpy.ops.pose.armature_apply(selected = False)      
        print('exiting pose mode')
        bpy.ops.object.mode_set(mode='OBJECT')                    
                        
    def clear_animation_data(self,skeleton_name):
        print('5. clear aniamation data') 
        
        print('    set animation to first frame')
        # Set the current frame to the first frame
        bpy.context.scene.frame_set(0)
        # Update the scene to reflect the change
        bpy.context.view_layer.update()
        
        '''
        skeleton_name.select_set(True)
        bpy.context.view_layer.objects.active = skeleton_name 
        bpy.ops.outliner.item_activate(deselect_all=True)
        bpy.ops.outliner.animdata_operation(type = 'CLEAR_ANIMDATA') 
        
        
        for window in bpy.context.window_manager.windows:
            screen = window.screenl

            for area in screen.areas:
                if area.type == 'OUTLINER':
                    override = bpy.context.copy()
                    override["area"] = area
                    bpy.ops.outliner.animdata_operation(override, type = 'CLEAR_ANIMDATA') 
                    break   
        '''                   
    # ---------------------------------------------------------------------------------------
    def reset_rest_pose_callback(self, context):
        # Perform some process when the button is clicked
        print(" - - - reset_rest_pose_callback - - - ")

        # init
        try:
            cc_skeleton_obj = bpy.data.scenes['Scene'].m_cc_skeleton
            cc_obj = self.get_armature_object_collection(self,cc_skeleton_obj.name)
            cc_obj.select_set(True)
            bpy.context.view_layer.objects.active = cc_obj
        except AttributeError:
            print('!!!  cc skeleton object error')
            return {'FINISHED'}
        
        self.set_animation_to_last_frame(self)
        self.generate_skeleton_to_shape_key(self,cc_obj)
        self.apply_skeleton_shape_key(self,cc_obj)
        self.apply_skeleton_to_restpose(self,cc_obj)
        self.clear_animation_data(self,cc_obj)
        
        return {'FINISHED'}



    def seperate_from_cc_object(self, cc_armature_obj, cc_armature):
        print('1. seperate facial bone from cc skeleton')
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='DESELECT')

        find_bone = False
        for bone in cc_armature.bones:
            if bone.name == self.cc_facial_bone_name:
                print("found facial bone")
                bone.select = True
                find_bone = True
                break
        bpy.ops.object.mode_set(mode='EDIT')
        
        if find_bone == False:
            print('facial bone not found')
            return
        #bpy.ops.armature.select_all()
        #bpy.ops.armature.select_hierarchy(direction='CHILD', extend=True)
        cc_armature.edit_bones.active = bpy.data.armatures[cc_armature.name].edit_bones[self.cc_facial_bone_name]
        bpy.data.armatures[cc_armature.name].edit_bones[self.cc_facial_bone_name].select = True
        print(bpy.data.armatures[cc_armature.name].bones[self.cc_facial_bone_name])
        bpy.ops.armature.select_similar(type='CHILDREN')
        
        print('selected bones:')
        for bone in bpy.context.selected_bones:
            print("  ",bone.name)
        
        # Detach the selected bones into a new skeleton
        bpy.ops.armature.separate()
        # Rename the new skeleton to "Amarture_Head"
        new_cc_head_armature = bpy.data.armatures[-1]
        new_cc_head_armature.name = self.cc_new_facial_skeleton_name

        # Switch back to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        return new_cc_head_armature


    def attach_to_bip(self, biped_armature, cc_head_armature):
        print('2. add cc_head to bip skeleton')
        
        if biped_armature is None or cc_head_armature is None:
            print('armature null:', biped_armature, ' and ',cc_head_armature)
            return
        
        biped_armature_obj = self.get_armature_object_collection(self,biped_armature.name)
        cc_head_armature_obj = self.get_armature_object_collection(self,cc_head_armature.name)
        '''
        if biped_armature_obj is None or cc_head_armature_obj is None:
            print('cannot find obj by armature name :', biped_armature.name, ' and ',cc_head_armature.name)
            return
        '''
        
        if biped_armature_obj is not None and cc_head_armature_obj is not None:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            biped_armature_obj.select_set(True)
            cc_head_armature_obj.select_set(True)
            bpy.context.view_layer.objects.active = biped_armature_obj
            print("selected obj type:", biped_armature_obj.type, ' and ', cc_head_armature_obj.type)
        
            bpy.ops.object.join()
        
        
        # 3. 进入骨骼编辑模式，将FacialBone父子连接到Bip001 Head 上
        facial_bone_real_name = None
        for bone in biped_armature.bones:
            #for test!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if bone.name.startswith(self.cc_facial_bone_name) and len(bone.name) == len(self.cc_facial_bone_name):
                continue
            
            if bone.name.startswith(self.cc_facial_bone_name):
                print("found facial bone")
                bone.select = True
                facial_bone_real_name = bone.name
                break
        
        if facial_bone_real_name == None:
            print('no facial bone found')
            return
        print('facial_bone_real_name :', facial_bone_real_name)
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')
        biped_armature_obj.select_set(True)
        # ##################IMPORTANT!!!!!  ##########
        # code below is vary important for
        # bpy.ops.armature.parent_set
        # otherwise it will report "RuntimeError: Error: Operation requires an active bone"
        bpy.context.view_layer.objects.active = biped_armature_obj
        ###############################################
        
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.armature.select_all(action='DESELECT')
        biped_armature = biped_armature_obj.data
        print(biped_armature.edit_bones)
        
        biped_armature.edit_bones.active = biped_armature.edit_bones[self.biped_head_attach_bone_name]
        biped_armature.bones.active = biped_armature.bones[self.biped_head_attach_bone_name]

        biped_armature.edit_bones[facial_bone_real_name].select = True
        biped_armature.edit_bones[self.biped_head_attach_bone_name].select = True
        bpy.context.object.data.edit_bones.active = biped_armature_obj.data.edit_bones[self.biped_head_attach_bone_name]
        bpy.ops.armature.parent_set(type='OFFSET')
        bpy.ops.armature.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')


    def move_mesh_to_biped_collection(self,mesh_obj):
        object_to_move = mesh_obj

        collection_from = bpy.data.collections["CC"]
        collection_to = bpy.data.collections["Biped"]

        collection_from.objects.unlink(object_to_move)
        collection_to.objects.link(object_to_move)    

    def transfer_vertex_data(self):
        print('3. transfer data')
        # 4. 退出骨骼编辑模式
        bpy.ops.object.mode_set(mode='OBJECT')
        biped_armature = bpy.data.scenes['Scene'].m_biped_skeleton

        # 4. CC骨骼下所有模型 父子连接到Biped骨骼上
        # 1. 选中CC骨骼下所有关联模型
        biped_armature_obj = self.get_armature_object_collection(self,biped_armature.name)

        #target_skin_mesh = bpy.data.scenes['Scene'].m_target_skin_mesh
        target_normal_mesh = bpy.data.scenes['Scene'].m_target_normal_mesh
        
        mesh_count = max(0, min(10, bpy.data.scenes['Scene'].sna_mesh_amount))
        print("mesh_count:",mesh_count)
        for i in range(1, mesh_count + 1):  # Loop from 1 to 10
            prop_name = f"sna_ccmesh{i:02d}"
            prop_sk_name = f"sna_sk{i:02d}"
            prop_no_name = f"sna_no{i:02d}"
            mesh_obj = bpy.data.scenes['Scene'].get(prop_name)
            mesh_skin_copy = bpy.data.scenes['Scene'].get(prop_sk_name)
            mesh_normal_copy = bpy.data.scenes['Scene'].get(prop_no_name)
            
            
            if mesh_obj:
                print('    mesh:',i,':',mesh_obj.name, " skin:", mesh_skin_copy, " normal:", mesh_normal_copy)
            else:
                continue
            
            bpy.ops.object.select_all(action='DESELECT')
            mesh_obj.select_set(True)
            bpy.context.view_layer.objects.active = mesh_obj
            # 5. 传递Biped头部骨骼权重至CC头部模型
            
            bpy.ops.object.modifier_add(type='DATA_TRANSFER')
            bpy.context.object.modifiers["DataTransfer"].object = target_normal_mesh
            if mesh_skin_copy :
                print('    mesh:',i,' copy skin')
                bpy.context.object.modifiers["DataTransfer"].use_vert_data = True
                bpy.context.object.modifiers["DataTransfer"].data_types_verts = {'VGROUP_WEIGHTS'}
            if mesh_normal_copy:  
                print('    mesh:',i,' copy normal') 
                bpy.context.object.modifiers["DataTransfer"].use_loop_data = True
                bpy.context.object.modifiers["DataTransfer"].data_types_loops = {'CUSTOM_NORMAL'}
            mod = bpy.context.object.modifiers["DataTransfer"]
            bpy.ops.object.datalayout_transfer(modifier = mod.name)    
            #bpy.ops.object.modifier_apply(modifier = mod.name)
            
            #cancel parent object scale
            bpy.ops.object.select_all(action='DESELECT')
            mesh_obj.select_set(True)
            bpy.context.view_layer.objects.active = mesh_obj
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            
            print("    move mesh{i:02d} to target armature")
            #move to biped armature
            bpy.ops.object.select_all(action='DESELECT')
            mesh_obj.select_set(True)
            biped_armature_obj.select_set(True)
            bpy.context.view_layer.objects.active = biped_armature_obj
            bpy.ops.object.parent_set(type='ARMATURE')
            #move to biped collection
            self.move_mesh_to_biped_collection(self,mesh_obj)

    #------------------------------------------------------------------------------ 
    def change_cc_head_callback(self, context):
        # Perform some process when the button is clicked
        print(" - - - change_cc_head_callback - - - ")
        

        # init
        try:
            cc_skeleton_obj = bpy.data.scenes['Scene'].m_cc_skeleton
            cc_obj = self.get_armature_object_collection(self,cc_skeleton_obj.name)
            cc_obj.select_set(True)
            bpy.context.view_layer.objects.active = cc_obj
        except AttributeError:
            print('!!!  cc skeleton object error')
            return {'FINISHED'}
        
        biped_armature = bpy.data.scenes['Scene'].m_biped_skeleton
        new_cc_head_armature = self.seperate_from_cc_object(self,cc_obj, cc_skeleton_obj)
        if new_cc_head_armature is None:
            new_cc_head_armature = bpy.data.armatures[self.cc_new_facial_skeleton_name]
        
        self.attach_to_bip(self,biped_armature, new_cc_head_armature)
        self.transfer_vertex_data(self)
        
        
        return {'FINISHED'}