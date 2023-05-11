<template>
   <ion-item-group>
    <ion-button @click="addNewClient($event)">add  client </ion-button>
    <ion-button @click="addNewVaccine($event)">add vaccine </ion-button>
    <ion-button @click="addNewDisease($event)">add disease</ion-button>
    <ion-button @click="displayVaccineInfo($event)">vaccination chart</ion-button>
    <ion-button @click="displayClientDetails($event)">display client details</ion-button>
    <!-- <ion-button @click="createInsilationGroup($event)">insolation group</ion-button> -->
  </ion-item-group>
   <ion-alert :is-open="isOpen" header="Alert" :message="alertMessage" :buttons="alertButtons" @didDismiss="setOpen(false)"></ion-alert>

   <ion-content v-if="displayVaccine" class="custom-content">
    <ion-item-group>
      <ion-item>
        <ion-title>{{ title }}</ion-title>
      </ion-item>
  <ion-item>
    <Chart/>
  </ion-item>
</ion-item-group>
    </ion-content>
  
 <GoogleMap v-if="insilationGroup"/>
  

  <ion-content v-if="addVaccine" class="custom-content">
    <ion-item><ion-title>{{ title }}</ion-title></ion-item>
    <ion-item-group >
      <ion-item><ion-input placeholder="ID*" v-model="client_id" maxLength="9"  @input="idValidation"></ion-input>
        <span v-if="idError" class="error">{{ idError }}</span></ion-item>
      <ion-item><ion-input placeholder="Manufacturer*" v-model="manufacturer" maxLength="255"></ion-input></ion-item>
  <ion-item>
    <p>Date</p>
    <ion-datetime picker-format="DD/MM/YYYY" display-format="DD/MM/YYYY" placeholder="Select Date" v-model="date"></ion-datetime>
  </ion-item>
  <ion-item> <ion-button :disabled="!isFormValid" @click="SubmitEvent">submit</ion-button></ion-item>
    </ion-item-group>
    </ion-content>
  

    <ion-content v-if="addDisease" class="custom-content">
      <ion-item><ion-title>{{ title }}</ion-title></ion-item>
    <ion-item-group >
      <ion-item><ion-input placeholder="ID*" v-model="client_id" maxLength="9"  @input="idValidation"></ion-input>
        <span v-if="idError" class="error">{{ idError }}</span></ion-item>
  <ion-item>
    <p>Positive date</p>
    <ion-datetime picker-format="DD/MM/YYYY" display-format="DD/MM/YYYY" placeholder="Select Date" v-model="positive_date"></ion-datetime>
    <p>Recovery date</p>
    <ion-datetime picker-format="DD/MM/YYYY" display-format="DD/MM/YYYY" placeholder="Select Date" v-model="recovery_date"></ion-datetime>
  </ion-item>
  <ion-item> <ion-button :disabled="!isFormValid" @click="SubmitEvent">submit</ion-button></ion-item>
    </ion-item-group>
    </ion-content>

    <ion-content v-if="addClient" class="custom-content">
      <ion-item><ion-title>{{ title }}</ion-title></ion-item>
        <ion-item-group >
        <ion-item>
          <ion-item><ion-input placeholder="ID*" v-model="client_id" maxLength="9"  @input="idValidation"></ion-input>
        <span v-if="idError" class="error">{{ idError }}</span></ion-item>
  </ion-item>
  <ion-item>
    <ion-input placeholder="First name*" v-model="first_name" maxLength="255"></ion-input>
    <ion-input placeholder="Last name*" v-model="last_name" maxLength="255"></ion-input>
  </ion-item>
  <ion-item>
    <ion-input placeholder="City*" v-model="city" maxLength="255"></ion-input>
    <ion-input placeholder="Street*" v-model="street" maxLength="255"></ion-input>
    <ion-input placeholder="House number*" v-model="house_number" maxLength="20"></ion-input>
  </ion-item>
  <ion-item>
    <ion-input placeholder="Phone number*" :counter="true" v-model="phone" maxLength="9" @input="validatePhone"></ion-input>
    <span v-if="phoneError" class="error">{{ phoneError }}</span>
    <ion-input placeholder="Cellular*" :counter="true" maxLength="10" v-model="cellular" @input="validateCellularNumber"></ion-input>
    <span v-if="cellularError" class="error">{{ cellularError }}</span>
  </ion-item>
  <ion-item>
    <p>Born date</p>
    <ion-datetime :disabled="!isFormValid" picker-format="DD/MM/YYYY" display-format="DD/MM/YYYY" placeholder="Select Date" v-model="date"></ion-datetime>
  </ion-item>
  <ion-item>
        <ion-button :disabled="!isFormValid" @click="SubmitEvent">submit</ion-button>
    </ion-item>
    </ion-item-group>
    </ion-content>
  
   
    <ion-content v-if="displayClient" class="custom-content">
      <ion-item><ion-title>{{ title }}</ion-title></ion-item>
        <ion-item-group >
        <ion-item>
          <ion-item><ion-input placeholder="ID*" v-model="client_id" maxLength="9"  @input="idValidation"></ion-input>
          <span v-if="idError" class="error">{{ idError }}</span></ion-item>
        <ion-item>
        <ion-button @click="displayEvent">display</ion-button>
    </ion-item>
  </ion-item>

  <ion-card  v-if="hasClient">
    <ion-card-header>
    <ion-card-title>{{ this.last_name}} {{ this.first_name}}</ion-card-title>
      <ion-card-subtitle>{{ this.client_id}}</ion-card-subtitle>
     </ion-card-header>
     <ion-card-content>
      <p class="new-line">address: {{ this.city }}, {{ this.street }}  {{ this.house_number }} </p>
      <p class="new-line"> phone number: {{ this.phone }}</p>
      <p class="new-line">Tcellular number: {{ this.cellular }}</p>
      <p class="new-line">born date: {{ this.date }} </p>   
    </ion-card-content>
     </ion-card>
      <ion-card  v-if="hasClient">
     <ion-card-header>
      <ion-card-subtitle>Covid19 details</ion-card-subtitle>
    </ion-card-header>
    <ion-card-content>
      <p class="new-line">positive date: {{ this.positive_date }}</p>
      <p class="new-line">recovery date: {{ this.recovery_date }}</p> 
    </ion-card-content>
  </ion-card>
  <ion-card v-for="item in jsonData" :key="item.client_id">
      <ion-card-content>
        <ion-card-subtitle>Vaccine Number: {{ item.vaccine_number }}</ion-card-subtitle>
        <p>Manufacturer: {{ item.manufacturer }}</p>
        <p>Date: {{ item.date }}</p>
      </ion-card-content>
    </ion-card>
    </ion-item-group>
    
    </ion-content>
  </template>
  
  <script lang="ts">
    import { defineComponent, ref  } from 'vue';
    import { IonAlert, IonButton,IonDatetime,IonInput,IonCard, IonCardContent, IonCardHeader, IonCardSubtitle, IonCardTitle } from '@ionic/vue';
    import axios from 'axios';
    import Chart from './Chart.vue'
    import GoogleMap from './GoogleMap.vue';
    import dayjs from 'dayjs';
    export default defineComponent({
      components: {GoogleMap,IonButton, IonDatetime, IonInput, IonCard, IonCardContent, IonCardHeader, IonCardSubtitle, IonCardTitle,Chart },
      data() {
    return {
        jsonData: [] as { client_id: number; manufacturer: string; date: string; vaccine_number: number }[],
        hasClient: false,
        addClient: false,
        addVaccine: false,
        addDisease: false,
        displayClient: false,
        displayVaccine: false,
        insilationGroup: false,
        cellularError:'',
        phoneError: '',
        idError: '',
        street:'',
        house_number:'',
        client_id: '',
        first_name: '',
        last_name: '',
        phone: '',
        city: '',
        cellular:'',
        manufacturer:'',
        date: this.getCurrentDate(),
        recovery_date: this.getCurrentDate(),
        positive_date: this.getCurrentDate(),
        isOpen : ref(false),
        alertMessage: "",
        title: '',
    };
  },
  computed: {
    isFormValid() {
      // Check all validations and return true if all are valid
      return this.phoneError == '' && this.idError == '' && this.cellularError == ''
    },
  },
  setup() {
      const isOpen = ref(false);
      const alertButtons = ['OK'];
      const setOpen = (state: boolean) => {
        isOpen.value = state;
      };

      return { isOpen, alertButtons, setOpen };
    },
  methods:  { 
    processJSONData(jsonData) {
      // Process each JSON object and create separate objects
      for (let i = 0; i < jsonData.length; i++) {
        const item = jsonData[i];
        // Create a new object for each item
        const newObj = {
          manufacturer: item.manufacturer,
          date: item.date,
          vaccine_number: i+1
        };
        // Push the new object to the jsonData array
        this.jsonData.push(newObj);
      }
    },
    
    fetchCovid()
    {
      // covid info
      axios.defaults.baseURL = 'http://127.0.0.1:5000';
       this.positive_date = "No information"
              this.recovery_date = "No information"
              axios.get(`/covid/info/${this.client_id}`)
             .then(response => {
              if (response.status === 201) 
              { 
                this.createCovidInfo(response.data);
              } 
            })
            .catch(error => {
            if (error.response && error.response.status === 400) {
            // Handle the 400 error response
            this.alertMessage = error.response.data;
            this.setOpen(true);
           }else {
            // Handle other errors
            console.error('An error occurred:', error);
          }
         })
    },

    formatDateTime(date) {
      const formatted = dayjs(date).format('DD/MM/YYYY');
      return formatted
    },
    validationForId(ID) {
      if (ID.length !== 9) {
        return false;
      }

      const IdList: number[] = [];

      try {
        for (let i = 0; i < ID.length; i++) {
          IdList.push(parseInt(ID[i], 10));
        }
      } catch {
        return false;
      }

      let counter = 0;
      for (let i = 0; i < 9; i++) {
        IdList[i] *= (i % 2) + 1;
        if (IdList[i] > 9) {
          IdList[i] -= 9;
        }
        counter += IdList[i];
      }

      return counter % 10 === 0;
    },
    validatePhone() {
      const phonePattern = /^(0[23489]|0[57]\d|70|72|74|76|77|78|79)\d{7}$/; // Regular expression pattern for  phone number
      if (this.phone && !phonePattern.test(this.phone)) {
        this.phoneError = 'Invalid phone number';
      } else {
        this.phoneError = '';
      }
  },
  validateCellularNumber() {
      const regex = /^0(5\d|7[7-9]|77|78)\d{7}$/;
      if (regex.test(this.cellular)) {
        this.cellularError = '';
      } else {
        this.cellularrError = 'Invalid cellular number';
      }
    },
    idValidation() {
      if (this.client_id && !this.validationForId(this.client_id)) {
        this.idError = 'Invalid ID';
      } else {
        this.idError = '';
      }
    },
    createClient(jsonData) {
      this.first_name   = jsonData.first_name;
      this.last_name    = jsonData.last_name;
      this.city         = jsonData.city;
      this.street       = jsonData.street;
      this.house_number = jsonData.house_number;
      this.phone        = jsonData.phone_number;
      this.cellular     = jsonData.cellular;
      this.date         = jsonData.born_date;
    },
    createCovidInfo(jsonData)
    {
      this.positive_date = jsonData.positive_date
      this.recovery_date = jsonData.recovery_date
    },
// get the current date in YYYY-MM-DD format
    getCurrentDate() {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const day = String(now.getDate()).padStart(2, '0');
      this.currentDate = `${year}-${month}-${day}`;
    },
    // Hide the other options
    hideAll()
    {
      this.displayVaccine  = false
      this.addClient       = false
      this.addDisease      = false
      this.addVaccine      = false
      this.hasClient       = false
      this.displayClient   = false
      this.insilationGroup = false
      this.clearInputs()
    },
    createInsilationGroup(event)
    {
      this.title = event.target.innerText;
      if(this.insilationGroup == true)
      {
        this.hideAll()
        this.insilationGroup = false
      }
      else{
        this.hideAll()
        this.insilationGroup = true
      }
    },
    displayVaccineInfo(event)
    {
      this.title = event.target.innerText;
      if(this.displayVaccine == true)
      {
        this.hideAll()
        this.displayVaccine = false
      }
      else{
        this.hideAll()
        this.displayVaccine = true
      }
    },
    displayClientDetails(event)
    {
      this.title = event.target.innerText;
      if(this.displayClient == true)
      {
        this.hideAll()
        this.displayClient = false
      }
      else{
        this.hideAll()
        this.displayClient = true
      }
    },
    addNewVaccine(event)
    {
      this.title = event.target.innerText;
      if(this.addVaccine == true)
      {
        this.hideAll()
        this.addVaccine = false
      }
      else{
        this.hideAll()
        this.addVaccine = true
      }
    }, 
    addNewClient(event)
    {
      this.title = event.target.innerText;
      if(this.addClient == true)
      {
        this.hideAll()
        this.addClient = false
      }
      else{
        this.hideAll()
        this.addClient = true
      }
    },
    addNewDisease(event)
    {
      this.title = event.target.innerText;
      if(this.addDisease == true)
      {
        this.hideAll()
        this.addDisease = false
      }
      else{
        this.hideAll()
        this.addDisease = true
      }
    },
    clearInputs()
    {
        this.client_id       = '',
        this.first_name      = '',
        this.last_name       = '',
        this.city            = '',
        this.house_number    = '',
        this.street          = '',
        this.phone           = '',
        this.cellular        ='',
        this.manufacturer    ='',
        this.phoneError      = ''
        this.idError         = ''
        this.cellularError   = ''
        this.jsonData        = []
        this.date = this.getCurrentDate()
        this.positive_date = this.getCurrentDate()
        this.recovery_date = this.getCurrentDate()
    },
      customFormatter(inputLength, maxLength) {
        return `${maxLength - inputLength} characters remaining`;
      },
      fetchVaccinations()
      {
        axios.defaults.baseURL = 'http://127.0.0.1:5000';
         // vaccintions list
         axios.get(`/get/vaccines_list/${this.client_id}`)
             .then(response => {
              if (response.status === 201) 
              { 
                this.processJSONData(response.data); 
              } 
            })
            .catch(error => {
            if (error.response && error.response.status === 400) {
            // Handle the 400 error response
            this.alertMessage = error.response.data;
            this.setOpen(true);
           }else {
            // Handle other errors
            console.error('An error occurred:', error);
          }
         })
      },
      displayEvent()
      {
        axios.defaults.baseURL = 'http://127.0.0.1:5000';
        if (this.displayClient == true)
        {
          if (this.client_id!='')
          {
            axios.get(`/get/client/${this.client_id}`)
            .then(response => {
              if (response.status === 201) 
              { 
                this.hasClient = true
                this.createClient(response.data);
                this.fetchCovid()
                this.fetchVaccinations()

              } 
            })
           
          .catch(error => {
            if (error.response && error.response.status === 400) {
            // Handle the 400 error response
            this.alertMessage = error.response.data;
            this.setOpen(true);
           }else {
            // Handle other errors
            console.error('An error occurred:', error);
          }
         })
          }
          else
           { 
            // show alert
            this.alertMessage = "ID ​​must be filled!"
            this.setOpen(true)
           }
        }
      },
      SubmitEvent()
      {
        axios.defaults.baseURL = 'http://127.0.0.1:5000';
        if (this.addClient == true)
        {
          if (this.client_id!='' && this.first_name!='' && this.last_name!=''&& this.house_number!=''&& this.street!='' && this.city!='' && this.phone!='' && this.cellular!='' && this.date)
           {
            const newClient = {
              client_id: this.client_id,
              first_name: this.first_name,
              last_name: this.last_name,
              city: this.city,
              street: this.street,
              house_number: this.house_number,
              phone_number: this.phone,
              cellular: this.cellular,
              born_date: this.formatDateTime(this.date),
            };
         axios.post('/add_client', newClient)
          .then(response => {
            this.alertMessage = response.data
              this.setOpen(true)
              if (response.status === 201) 
              { 
                this.addClient = false 
                this.clearInputs()
              } 
            })
          .catch(error => {
            if (error.response && error.response.status === 400) {
            // Handle the 400 error response
            this.alertMessage = error.response.data;
            this.setOpen(true);
           }else {
            // Handle other errors
            console.error('An error occurred:', error);
          }
         })
          }else{ 
          // show alert
          this.alertMessage = "All inputs ​​must be filled!"
          this.setOpen(true)}
        }else if (this.addVaccine == true){
           if (this.client_id!='' && this.manufacturer!='' && this.date)
            {
              const newVaccine = {
              client_id: this.client_id,
              manufacturer: this.manufacturer,
              date:  this.formatDateTime(this.date),
              vaccine_number: -1
              };
             axios.post('/add_vaccine', newVaccine)
             .then(response => {
              this.alertMessage = response.data
              this.setOpen(true)
              if (response.status === 201) 
              { 
                this.addVaccine = false 
                this.clearInputs()
              } 
              })
             .catch(error => {
             if (error.response && error.response.status === 400) {
             // Handle the 400 error response
             this.alertMessage = error.response.data;
             this.setOpen(true);
            }else {
            // Handle other errors
             console.error('An error occurred:', error);
              }
            })
            }
           else
           { 
            // show alert
            this.alertMessage = "All inputs ​​must be filled!"
            this.setOpen(true)
           }
        }
        else
        {
          if (this.client_id!='' && this.positive_date && this.recovery_date)
           {
            const newDisease = {
              client_id: this.client_id,
              positive_date:  this.formatDateTime(this.positive_date),
              recovery_date: this.formatDateTime(this.recovery_date),
            };
         axios.post('/add_covid', newDisease)
          .then(response => {
            this.alertMessage = response.data
              this.setOpen(true)
              if (response.status === 201) 
              { 
                this.addDisease = false 
                this.clearInputs()
              } 
            })
          .catch(error => {
            if (error.response && error.response.status === 400) {
            // Handle the 400 error response
            this.alertMessage = error.response.data;
            this.setOpen(true);
           }else {
            // Handle other errors
            console.error('An error occurred:', error);
          }
         })
          }else{ 
          // show alert
          this.alertMessage = "All inputs ​​must be filled!"
          this.setOpen(true)}
        }
      
      }
    }
    });
  </script>

  <style scoped>
  .new-line {
  margin-bottom: 10px; 
}
.custom-content {
  height: 600px; 
}
</style>