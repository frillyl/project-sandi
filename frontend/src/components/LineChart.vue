<template>
  <Line :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
)

const props = defineProps({
  chartData: Object,
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        color: '#333',
      },
    },
  },
  scales: {
    x: {
      ticks: {
        color: '#555',
      },
    },
    y: {
      beginAtZero: true,
      ticks: {
        color: '#555',
        stepSize: 1,
        callback: function (value) {
          return Number.isInteger(value) ? value : ''
        },
      },
    },
  },
}
</script>

<style scoped>
:deep(canvas) {
  max-height: 350px;
}
</style>
