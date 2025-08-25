<script>
    import Card from './card.svelte'
</script>
<div style = "height:1000px;" class = "items-center justify-center">
<h1 class = "text-center text-stone-700 dark:text-white text-9xl madimi mb-20">Our Solutions</h1>
<div class="flex flex-row justify-center items-center ">
   <div class = "flex flex-col items-center justify-center flex-grow w-2/3">
    <a href = "./case1">    
    <figure style="--c:#fff5">
        <img src="solution1.jpg" width = 420 alt="Mountains">
            <figcaption>Try It Out</figcaption>
        </figure>
   
    </a>
    <Card data = {"Upload images of any area over a period of time and this model will analyse the Deforestation percentages over a period of time"} title = {"Analysis"}/>
    </div>


   <div class = "flex flex-col items-center justify-center flex-grow w-2/3">
    <a href = "./case2">
        <figure style="--c:#fff5">
           <img src="/types.jpg" alt="Mountains"  width=430 >
            <figcaption>Try it out</figcaption>
        </figure>
    </a>
    <Card data = {"Upload images of an area and our model will determine the type of deforestation"} title = {"Types of Deforestation"}/>
</div>
<div class = "flex flex-col items-center justify-center flex-grow w-2/3">
    <a href = "/fromOurEnd">    
    <figure style="--c:#fff5">
           <img src="plant.jpg" width = 550 alt="Mountains">
            <figcaption>How you can help?</figcaption>
        </figure>
   
    </a>
    <Card data = {"What all can be done on your behalf for the welfare of our nature"} title = {"Your Support"}/>
    </div>

</div>
</div>
<style>
    figure {
  display: grid;
  border-radius: 1rem;
  overflow: hidden;
  cursor: pointer;
}
figure > * {
  grid-area: 1/1;
  transition: .4s;
}
figure figcaption {
  display: grid;
  align-items: end;
  font-family: sans-serif;
  font-size: 2.3rem;
  font-weight: bold;
  color: #0000;
  padding: .75rem;
  background: var(--c,#0009);
  clip-path: inset(0 var(--_i,100%) 0 0);
  -webkit-mask:
    linear-gradient(#000 0 0),
    linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  -webkit-mask-clip: text, padding-box;
  margin: -1px;
}
figure:hover figcaption{
  --_i: 0%;
}
figure:hover img {
  transform: scale(1.2);
}
@supports not (-webkit-mask-clip: text) {
  figure figcaption {
   -webkit-mask: none;
   color: #fff;
  }
}

</style>