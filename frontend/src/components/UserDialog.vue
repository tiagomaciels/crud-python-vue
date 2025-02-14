<template>
    <v-dialog v-model="dialog" max-width="600" persistent>
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ editUser ? 'Edit User' : 'Create User' }}</span>
        </v-card-title>
  
        <v-card-text>
          <v-form ref="formRef" @submit.prevent="saveUser" v-model="isFormValid">
            <v-text-field
              label="Username"
              v-model="formData.username"
              :rules="[rules.required]"
              required
            ></v-text-field>
  
            <v-text-field
              label="Password"
              type="password"
              v-model="formData.password"
              :rules="[rules.required]"
              required
            ></v-text-field>
  
            <v-select
              label="Roles"
              v-model="formData.roles"
              :items="allRoles"
              multiple
            ></v-select>
  
            <v-switch
              label="Active?"
              v-model="formData.active"
              :color="formData.active ? 'green' : 'red'"
            ></v-switch>
  
            <v-text-field
              label="Timezone"
              v-model="formData.timezone"
              :rules="[rules.required]"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
  
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Cancel</v-btn>
          <v-btn text color="primary" @click="saveUser" :disabled="!isFormValid">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script>
  import { ref, watch } from 'vue';
  import { createUser, updateUser } from '@/api/users';
  
  export default {
    name: 'UserDialog',
    props: {
      editUser: {
        type: Object,
        default: null,
      },
    },
    emits: ['close', 'save'],
    setup(props, { emit }) {
      const dialog = ref(true);
      const formRef = ref(null);
      const isFormValid = ref(false);
      const rules = {
        required: value => !!value || 'This field is required',
      };
      const formData = ref({
        username: '',
        password: '',
        active: true,
        roles: [],
        timezone: '',
      });
  
      const allRoles = ref(['admin', 'manager', 'tester']);
  
      watch(
        () => props.editUser,
        (newVal) => {
          if (newVal) {
            formData.value = {
              username: newVal.username,
              password: newVal.password,
              active: newVal.active,
              roles: newVal.roles,
              timezone: newVal.preferences?.timezone || '',
            };
          } else {
            formData.value = {
              username: '',
              password: '',
              active: true,
              roles: [],
              timezone: '',
            };
          }
        },
        { immediate: true }
      );
  
      const closeDialog = () => {
        dialog.value = false;
        emit('close');
      };
  
      const saveUser = async () => {
            try {
              const isValid = await formRef.value?.validate();
        
              if (!isValid) {
                return;
              }

              if (props.editUser) {
                if (window.confirm(`Are you sure you want to save user ${formData.value.username}?`)) {
                    await updateUser(props.editUser.id, {
                    user: formData.value.username,
                    password: formData.value.password,
                    is_user_active: formData.value.active,
                    is_user_admin: formData.value.roles.includes('admin'),
                    is_user_manager: formData.value.roles.includes('manager'),
                    is_user_tester: formData.value.roles.includes('tester'),
                    user_timezone: formData.value.timezone,
                    });
                }
              } else {
                await createUser({
                  user: formData.value.username,
                  password: formData.value.password,
                  is_user_active: formData.value.active,
                  is_user_admin: formData.value.roles.includes('admin'),
                  is_user_manager: formData.value.roles.includes('manager'),
                  is_user_tester: formData.value.roles.includes('tester'),
                  user_timezone: formData.value.timezone,
                });
              }
              emit('save');
              closeDialog();
            } catch (err) {
              console.error('Error saving user:', err);
            }
        
      };
  
      return {
        dialog,
        formRef,
        formData,
        allRoles,
        isFormValid,
        rules,
        closeDialog,
        saveUser,
      };
    },
  };
  </script>
  