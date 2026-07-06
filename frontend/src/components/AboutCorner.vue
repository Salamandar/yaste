<template>
  <div id="corner-about">
    <div class="corner-div">
       <a href="https://github.com/salamandar/yaste" target="_blank">
        <img alt="Vue logo" class="logo" src="../assets/logo.svg" />
       </a>
    </div>
  </div>
</template>

<style scoped>
#corner-about {
  position: fixed;
  top: 0px;
  right: 0px;
  z-index: +1000;
  background: rgba(0,0,0,0.1);
  user-select: none;
}

.corner-div {
  padding: 10px;
  text-align: center;
}

.corner-div a {
  display: inline-block;
  margin: 0px;
}

.corner-div .logo {
  height: 20px;
  vertical-align: center;
}

.logo {
  filter: invert(42%) sepia(93%) saturate(500%) hue-rotate(120deg) brightness(119%) contrast(119%);
}


a,
.green {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.4s;
  padding: 3px;
}


@media (hover: hover) {
  a:hover {
    background-color: hsla(160, 100%, 37%, 0.2);
  }
}


</style>
