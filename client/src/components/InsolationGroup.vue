<template>
    
   
  <div>
    <!-- <DatePicker v-model="selectedDate"  />
    <p>Selected date: {{ selectedDate }}</p> -->
  </div>
  <div>
     
<div class="q-pa-md row items-start q-gutter-md">
  <q-card class="my-card">
      <div ref="map" style="height: 500px;"></div>

    <q-card-section>
      <input type="text" v-model="searchQuery" @keydown.enter="searchLocation">
      <button @click="searchLocation">Search</button>
      <q-btn label="search location" type="submit" color="primary" @click="searchLocation"/>
    </q-card-section>

    <div class="q-pa-md">
  <div class="q-gutter-md row items-start">
    <q-date v-model="date" />

    <q-date
      v-model="date"
      minimal
    />
  </div>
</div>
  </q-card>
</div>
  </div>
</template>

<script>
// import DatePicker from 'vue3-datepicker';
import  IsolationGroup  from '../utils/isolationGroup'

export default {
  // components: { DatePicker  },
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