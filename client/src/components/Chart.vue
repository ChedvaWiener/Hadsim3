  <template>
    <div>
        <p>number of vaccinations accinations</p>
      <canvas ref="chartRef" style="width: 200px; height: 200px;"></canvas>
    </div>
  </template>
  <script>
  import { ref, onMounted } from 'vue';
  import { Chart, registerables } from 'chart.js';
  import axios from 'axios';
  
  export default {
    setup() {
      const chartRef = ref(null);
  
      onMounted(async () => {
        Chart.register(...registerables);
        const canvas = chartRef.value;
  
        if (canvas) {
          try {
            const response = await axios.get('http://127.0.0.1:5000//vaccine/data');
            const data = response.data;
  
            const ctx = canvas.getContext('2d');
            new Chart(ctx, {
              type: 'doughnut',
              data: {
                labels: data.labels,
                datasets: [
                  {
                    data: data.values,
                    backgroundColor: data.colors,
                  },
                ],
              },
            });
          } catch (error) {
            console.error(error);
          }
        }
      });
  
      return {
        chartRef,
      };
    },
  };
  </script>
  