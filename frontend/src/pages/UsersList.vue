<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="text-h4">Users</h1>
      </v-col>
      <v-col class="text-end">
        <v-btn color="primary" @click="openCreateDialog">
          Create User
        </v-btn>
      </v-col>
    </v-row>

    <v-data-table
      :items="users"
      :headers="headers"
      class="elevation-1"
      :items-per-page="10"
    >
      <template #[`item.username`]="{ item }">
        <router-link :to="`/users/${item.id}`">
          {{ item.username }}
        </router-link>
      </template>

      <template #[`item.roles`]="{ item }">
        {{ item.roles ? item.roles.join(', ') : '' }}
      </template>

      <template #[`item.timezone`]="{ item }">
        {{ item.preferences?.timezone }}
      </template>

      <template #[`item.active`]="{ item }">
        <v-chip :color="item.active ? 'green' : 'red'" dark>
          {{ item.active ? 'Yes' : 'No' }}
        </v-chip>
      </template>

      <template #[`item.created_ts`]="{ item }">
        {{ item.created_ts }}
      </template>

      <template #[`item.actions`]="{ item }">
        <v-btn icon @click="openEditDialog(item)">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <v-btn icon @click="confirmDelete(item)">
          <v-icon color="red">mdi-delete</v-icon>
        </v-btn>
      </template>
    </v-data-table>

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
import { getAllUsers, deleteUser } from '@/api/users';
import UserDialog from '@/components/UserDialog.vue';

export default {
  name: 'UsersList',
  components: {
    UserDialog,
  },
  setup() {
    const users = ref([]);
    const showDialog = ref(false);
    const selectedUser = ref(null);

    const headers = [
      { title: 'Username', key: 'username' },
      { title: 'Roles', key: 'roles' },
      { title: 'Timezone', key: 'timezone' },
      { title: 'Is Active?', key: 'active' },
      { title: 'Created At', key: 'created_ts' },
      { title: 'Actions', key: 'actions', sortable: false },
    ];

    const loadUsers = async () => {
      try {
        const data = await getAllUsers();
        users.value = data;
      } catch (err) {
        console.error('Error loading users:', err);
      }
    };

    onMounted(() => {
      loadUsers();
    });

    const openCreateDialog = () => {
      selectedUser.value = null;
      showDialog.value = true;
    };

    const openEditDialog = (user) => {
      selectedUser.value = { ...user };
      showDialog.value = true;
    };

    const closeDialog = () => {
      showDialog.value = false;
    };

    const handleSave = () => {
      loadUsers();
      showDialog.value = false;
    };

    const confirmDelete = (user) => {
      if (window.confirm(`Are you sure you want to delete user ${user.username}?`)) {
        deleteUser(user.id)
          .then(() => {
            loadUsers();
          })
          .catch((err) => {
            console.error('Error deleting user:', err);
          });
      }
    };

    return {
      users,
      headers,
      showDialog,
      selectedUser,
      openCreateDialog,
      openEditDialog,
      closeDialog,
      handleSave,
      confirmDelete,
    };
  },
};
</script>

<style scoped>
</style>