<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="text-h4">User Details</h1>
      </v-col>
    </v-row>
    
    <v-row v-if="user">
      <v-col>
        <h2>{{ user?.username }}</h2>
        <p><strong>Roles:</strong> {{ user.roles.join(', ') }}</p>
        <p><strong>Timezone:</strong> {{ user.preferences?.timezone }}</p>
        <p><strong>Is Active?</strong> {{ user.active ? 'Yes' : 'No' }}</p>
        <p><strong>Created At:</strong> {{ user.created_ts }}</p>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-btn color="secondary" class="mr-2" @click="$router.push('/users')">
          <v-icon icon="mdi-arrow-left" class="mr-2"></v-icon>
          Back
        </v-btn>
        <v-btn color="primary" style="margin-right: 8px" @click="openEditDialog(user)">Edit</v-btn>
        <v-btn color="error" @click="confirmDelete(user)">Delete</v-btn>
      </v-col>
    </v-row>

    <user-dialog
      v-if="showDialog"
      :edit-user="selectedUser"
      @close="closeDialog"
      @save="handleSave"
    />
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getUserById, deleteUser } from '@/api/users';
import UserDialog from '@/components/UserDialog.vue';

export default {
  name: 'UserDetails',
  components: {
    UserDialog,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const user = ref(null);
    const showDialog = ref(false);
    const selectedUser = ref(null);

    const loadUser = async () => {
      try {
        const data = await getUserById(route.params.id);
        user.value = data;
      } catch (err) {
        console.error('Error loading user:', err);
      }
    };

    onMounted(() => {
      loadUser();
    });

    const openEditDialog = (u) => {
      selectedUser.value = { ...u };
      showDialog.value = true;
    };

    const closeDialog = () => {
      showDialog.value = false;
    };

    const handleSave = () => {
      loadUser();
      showDialog.value = false;
    };

    const confirmDelete = (u) => {
      if (window.confirm(`Are you sure you want to delete user ${u.username}?`)) {
        deleteUser(u.id)
          .then(() => {
            router.push('/users'); 
          })
          .catch((err) => {
            console.error('Error deleting user:', err);
          });
      }
    };

    return {
      user,
      showDialog,
      selectedUser,
      loadUser,
      openEditDialog,
      closeDialog,
      handleSave,
      confirmDelete,
    };
  },
};
</script>
