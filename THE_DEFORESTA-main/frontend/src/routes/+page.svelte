<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    overflow-x:hidden;
    overflow-y: hidden;
}
.page-content {
        position: relative;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index:1;
    }
.parallax{
    display: flex;
    justify-content: center;

    height:100vh;

}

#text
{
    position: absolute;
    font-size: 10em;
}
.parallax img
{
    position:absolute;
    top:0%;
    left:0%;
    width:100%;
    pointer-events: none;
}
.sec
{
    position: relative;
    padding:0px;
    margin-top:100px;
}
</style>
<script>
import { onMount} from 'svelte';
import Solutions from "./solutions/+page.svelte"
import { lght } from './lightdark.js';
let light;
console.log(lght);  // Log lght to the console
  lght.subscribe((value) => {
    light = value;
  });

let text;
let leaf;
let hill1;
let hill4;
let hill5;

onMount(() => {
    window.addEventListener('scroll',() => {
        let value = window.scrollY;
        text.style.marginTop = value * 2.5 + 'px';
        hill5.style.left = value * 1.5 + 'px';
        hill4.style.left = value * -1.5 + 'px';
        hill1.style.top = value * 1 + 'px';
    })
});

</script>
<div class = "page-content">
<section class = "parallax">
    <img src = "hill1.png" id = "hill1" bind:this={hill1}>
    <img src = "hill2.png" id = "hill2">
    <img src = "hill3.png" id = "hill3">
    <img src = "hill4.png" id = "hill4" bind:this={hill4}>
    <img src = "hill5.png" id = "hill5" bind:this={hill5}>
    <img src = "tree.png" id = "tree">
    <p class = "madimi text-green-900 dark:text-white" id = "text" bind:this={text}>Vanishing Greens</p>
    <img src = "plant.png" id = "plant">
</section>
<section class = "sec bg-amber-100 dark:bg-gray-700" >

   

    <div style = "height: 800px;" class="overflow-hidden w-full">
        {#if light=="dark"}
          <img src="curvyDark.svg" class="w-full">
        {:else}
          <img src="curvyLight.svg" class="w-full">
        {/if}
      </div>
      <Solutions />
      <footer  class = "dark:text-white madimi text-xl ml-10 mr-10 w-full text-center">
        <p>Made By Code Monks</p>
      </footer>
</section>

</div>
