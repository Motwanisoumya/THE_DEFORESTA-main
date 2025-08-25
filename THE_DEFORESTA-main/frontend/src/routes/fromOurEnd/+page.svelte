<script>
  import Ab from './know.svelte'
</script>

<h1 class = "text-3xl dark:text-white text-9xl madimi mb-10">
  Our Mission
</h1>

<div class="grid grid-flow-row-dense gap-4 butto">
  <Ab head="Digitalization" body="Move paper-based processes to digital platforms to reduce the need for paper."/>
  <Ab head="Efficiency" body="Write efficient code to reduce the amount of processing power and energy required."/>
  <Ab head="Remote" body="Promote remote work to reduce the need for commuting and reduce carbon emissions."/>
  <Ab head="E-Waste" body="Manage electronic waste properly to prevent harmful substances from damaging the environment."/>
  <Ab head="Hosting" body="Use green web hosting services that use renewable energy or participate in carbon offsetting programs."/>
  <Ab head="Recycle" body="Recycle paper and cardboard products to reduce the need for new paper."/>
  <Ab head="Planting" body="Participate in tree planting initiatives in your local community."/>
  <Ab head="Education" body="Educate others about the importance of trees and how they can help save them."/>
  <Ab head="Conservation" body="Support conservation organizations that work to protect forests and other natural habitats."/>
  <Ab head="Policy" body="Advocate for policies that protect trees and forests."/>
  <Ab head="Reuse" body="Reuse paper products as much as possible before recycling or disposing of them."/>
  <Ab head="Awareness" body="Raise awareness about the importance of trees and the need for conservation."/>
</div>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
</style>