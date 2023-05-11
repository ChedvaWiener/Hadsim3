<template>
  <div>
    <ion-item></ion-item> 
   <div ref="map" style="height: 300px;"></div>
  <ion-item>
    <ion-input type="text" placeholder="Search location"  v-model="searchQuery" @keydown.enter="searchLocation"></ion-input>
    <ion-button @click="searchLocation">search</ion-button>
  </ion-item> 
  <ion-content v-if="addDisease" class="custom-content">
  <ion-item>
    <p>Date</p>
    <ion-datetime picker-format="DD/MM/YYYY" display-format="DD/MM/YYYY" placeholder="Select Date" :class="smaller-datetime"></ion-datetime>
   </ion-item>
  </ion-content>
  </div>
  </template>
  
  <script>
  import  IsolationGroup  from '../utils/isolationGroup'
  import {IonButton,IonDatetime,IonInput,IonCard, IonCardContent, IonCardHeader, IonCardSubtitle, IonCardTitle } from '@ionic/vue';
  import axios from 'axios';

  export default {
    components: {IonButton, IonDatetime, IonInput, IonCard, IonCardContent, IonCardHeader, IonCardSubtitle, IonCardTitle },
    methods: {
    searchLocation() {
      // Use the Google Maps Geocoding API to search for the location
      const geocoder = new google.maps.Geocoder();
      geocoder.geocode({ address: this.searchQuery }, (results, status) => {
        if (status === 'OK' && results.length > 0) {
          const location = results[0].geometry.location;
          this.markerPosition = { lat: location.lat(), lng: location.lng() };
          this.wkt = `POINT(${location.lng()} ${location.lat()})`;
          console.log(this.wkt); // log WKT to console
        } else {
          console.log('Location not found');
        }
      });
    },
    logSelectedDate() {
      console.log(this.selectedDate);
    }
  },
  data() {
    return {
      center: { lat: 37.7749, lng: -122.4194 }, // default map center
      zoom: 12, // default zoom level
      searchQuery: '',
      markerPosition: null,
      selectedDate: new Date(),
      wkt: ''
    };
  },
    mounted() {
    this.map = new google.maps.Map(this.$refs.map, { zoom: 8, center: { lat: 37.7749, lng: -122.4194 } });
  },
  computed: {
    myObject() {
        console.log(this.wkt)
      return IsolationGroup(this.wkt, this.selectedDate)
    }
  }
  };
  </script>

   <style scoped>
   .smaller-datetime {
    font-size: 12px;
  --padding-start: 4px;
  --padding-end: 4px;
  --min-width: 100px;
}
 .custom-content {
   height: 200px; 
 }
 </style>