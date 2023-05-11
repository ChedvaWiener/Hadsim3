<template>
    <form id="form" @submit.prevent="submit">
        <ion-item>
    <ion-item><ion-input type="file"  accept="image/*" @change="handleFileUpload"/></ion-item>
    <ion-item><ion-button  @click="uploadImage" :disabled="!selectedFile">Upload</ion-button></ion-item>
    <ion-item> <ion-img 
      :src="previewImage" v-if="previewImage" alt="Preview" class="preview-image"
  ></ion-img></ion-item>
</ion-item>
<p class="new-line">address: {{ this.address }}</p>
    </form>

  </template>
  
  <script>
  import { ref } from 'vue';
  import axios from 'axios';
  import { IonImg, IonAlert, IonButton,IonDatetime,IonInput,IonCard, IonCardContent, IonCardHeader, IonCardSubtitle, IonCardTitle } from '@ionic/vue';
  
  export default {
    components: { IonImg,IonAlert, IonButton,IonDatetime,IonInput,IonCard, IonCardContent, IonCardHeader, IonCardSubtitle, IonCardTitle },
    name: 'ImageUploader',
  data() {
    return {
      selectedFile: null,
      previewImage: null,
      address: "5t67yui"
    }
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file && file.type.startsWith('image/')) {
        this.selectedFile = file;
        this.previewImage = URL.createObjectURL(file);
      } else {
        this.selectedFile = null;
        this.previewImage = null;
      }
    },
    uploadImage() {
      formData.append('image', this.selectedFile);
      axios.defaults.baseURL = 'http://127.0.0.1:5000';

      const form = document.getElementById('form');
      const formData = new FormData(form);
      axios.post('/upload', formData)
        .then(response => {
          console.log('Image uploaded successfully');
          // Handle the response as needed
        })
        .catch(error => {
          console.error('Error uploading image:', error);
          // Handle the error
        });
    }
  }
};
</script>
  <style scoped>
  .preview-image {
  border-radius: 50%;
}
</style>