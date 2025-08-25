<script>
  import { lght } from './lightdark.js';
  import "../app.css";
  console.log("Here is ",lght)
  let light;

  // Subscribe to the lght store
  lght.subscribe((value) => {
    light = value;
  });
  function lights() {
    lght.update((n)=> n==""?"dark":"");
  }
  
</script>
<div class = "{light} layout-content">
<div class="bg-blue-100 dark:bg-gray-700 flex flex-col items-center">
    <nav class="flex flex-col sm:flex-row justify-between w-full p-10">
      <a href="/" class="font-bold text-4xl sm:text-6xl mb-4 sm:mb-0 flex items-center madimi dark:text-white"><img src = ./{light=="dark"?"logo2.png":"logo.png"} width = 150></a>
      <span class="space-x-0 sm:space-x-10 text-xl sm:text-sm anta-regular flex flex-col sm:flex-row ">
        <button on:click = {lights} class = "mb-8">
          {#if light=="dark"}
          <img src = "burned.png" alt = "Turn light on" class = "m-0  rounded-full">
          {:else}
          <img src = "torch-minecraft.gif" alt = "Turn light off" width="29" class = "m-0">
          {/if}
          </button>
        <a class = "text-4xl flex items-center dark:text-white buda" href="/solutions">Solutions</a>
        <a class = "text-4xl flex items-center dark:text-white buda" href="/fromOurEnd">Our Mission</a>
        <a href="/about" class=" buda text-3xl bg-green-600 dark:bg-blue-100 dark:text-black dark:hover:bg-blue-200 text-white rounded-md p-5 h-12 mt-12 leading-10 hover:bg-green-500 transi duration-200 flex items-center">About</a>
      </span>

    </nav>
  <slot />

  </div>
  
  </div>
  <style>
    .layout-content {
        position: relative;
    }
  </style>