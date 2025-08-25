<script>
  import Loading from "../loading.svelte";
  import Loading2 from "../loading2.svelte";
  let files;
  let imageUrls = [];
  let status = 1
  const uploadFiles = async () => {
    status = -1;
    if (!files || files.length === 0) {
      console.error('No files selected');
      return;
    }

    for (let file of files) {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const filename = await response.text();
        imageUrls.push(`http://localhost:5000/all_images/${filename}`);
        console.log('File uploaded successfully');
      } else {
        console.error('File upload failed');
      }
    }

    const scriptResponse = await fetch('http://localhost:5000/run_script', {
      method: 'POST',
    });


    if (scriptResponse.ok) {
      console.log('Script executed successfully');
    } else {
      console.error('Script execution failed');
    }
    status = 0;
  };
  function repeat() {
    imageUrls = [];
    status = 1;
    files = undefined;
  }
  let imgSrc1 = './solution/deforestation1.png';
  let imgSrc2 = './solution/deforestation2.png';
  function refreshImage() {
    imgSrc1 = './solution/deforestation1.png?' + new Date().getTime();
    imgSrc2 = './solution/deforestation2.png?' + new Date().getTime();
  }

  setTimeout(refreshImage, 500);
  function refreshWindow() {
    if (typeof window !== 'undefined') {
      window.location.reload();
    }
  }
</script>


  <div style = "height:980px;" class = "w-full flex flex-col items-center background">
  <h1 class="dark:text-white text-9xl mt-10 madimi mb-20">Deforestation Analysis</h1>
  
  {#if status == 0}
  <div class = "flex flex-row">
    <div class = "flex flex-col items-center text-2xl im2">
    <img src={imgSrc1}  width=900 class = "p-1 border border-black dark:border-white">
    <figcaption class = " paratext">Deforested Areas over the years</figcaption>
    </div>
    <div class = "flex flex-col items-center text-2xl im1">
    <img src = {imgSrc2} width=900 class = "p-1 border border-black dark:border-white">
    <figcaption class = " paratext">Graph Showing the Percentage of Deforestation</figcaption>
    </div>
  </div>
    <button on:click={refreshWindow} class="cu text-3xl bg-slate-300 dark:bg-slate-500 dark:hover:bg-blue-500 hover:bg-blue-300 rounded-md p-4 madimi dark:text-white">Try Again</button>
    {:else if status == -1}
    <Loading2 />
  {:else}
  <p class = "dark:text-white text-5xl paratext mb-20 w-2/3 text-center"> Upload images of any area over a period of time and this model will analyse the Deforestation percentages over a period of time</p>
    <label for="file" class="custom-file-label text-4xl rounded-md">Choose files</label>
    <input id="file" type="file" accept=".jpg" bind:files={files} class="custom-file-input" multiple />
  {#if files != undefined}
    <button on:click={uploadFiles} class="butto text-3xl bg-slate-300 dark:bg-slate-500 dark:hover:bg-blue-500 hover:bg-blue-300 rounded-md p-4 madimi dark:text-white mt-10">Upload</button>
    {/if}
    {/if}
    </div>

  <style>
    .custom-file-input {
      width: 0.1px;
      height: 0.1px;
      opacity: 0;
      overflow: hidden;
      position: absolute;
      z-index: -1;
    }
    .custom-file-label {
      padding: 10px;
      background-color: #4CAF50; /* Green background */
      color: white; /* White text */
      cursor: pointer; /* Pointer cursor on hover */
      border-radius: 10%;
    }
    .custom-file-label:hover {
      background-color: #94dd97; /* Darker green background on hover */
    }
    @keyframes slideDown {
    0% {
      opacity: 0;
      transform: translateY(100%);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }
  @keyframes slideLeft {
    0% {
      opacity: 0;
      transform: translateX(100%);
    }
    100% {
      opacity: 1;
      transform: translateX(0);
    }
  }
  @keyframes slideRight {
    0% {
      opacity: 0;
      transform: translateX(-100%);
    }
    100% {
      opacity: 1;
      transform: translateX(0);
    }
  }
  .background {
    background-image: url('./layertree.svg');
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center -450px;
    animation: slideDown 800ms ease-in-out 1; /* Adjust as needed */
  }
  .im1
  {
    animation: slideLeft 800ms ease-in-out 1;
  }
  .im2
  {
    animation: slideRight 800ms ease-in-out 1;
  }
  .butto
  {
    animation: slideDown 200ms ease-in-out 1;
  }

  </style>