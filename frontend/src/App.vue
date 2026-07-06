<script setup lang="ts">
  import TextArea from './components/TextArea.vue';
  import AboutCorner from './components/AboutCorner.vue';
</script>

<template>
  <AboutCorner />
  <TextArea />
</template>

<style scoped>
  @media (min-width: 1024px) {
    header {
      display: flex;
      place-items: center;
      padding-right: calc(var(--section-gap) / 2);
    }

    .logo {
      margin: 0 2rem 0 0;
    }

    header .wrapper {
      display: flex;
      place-items: flex-start;
      flex-wrap: wrap;
    }
  }
</style>
