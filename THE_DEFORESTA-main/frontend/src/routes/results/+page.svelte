// Results Page (results/+page.svelte)
<script>
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';

  let composites = [];
  let searchLocation = '';
  let optimalWindow = '';
  let skippedYears = [];
  let loading = false;
  let imageErrors = new Set();

  $: {
    // Parse URL parameters
    const urlParams = new URLSearchParams($page.url.search);
    const imagesStr = urlParams.get('images');
    searchLocation = urlParams.get('place') || 'Unknown Location';
    optimalWindow = urlParams.get('optimal_window') || '';
    const skippedYearsStr = urlParams.get('skipped_years') || '';
    skippedYears = skippedYearsStr ? skippedYearsStr.split(',').filter(Boolean) : [];

    if (imagesStr) {
      // Parse "year|filename.png" format
      composites = imagesStr.split(',').map(item => {
        const [year, filename] = item.split('|');
        return { year, filename, loaded: false };
      }).sort((a, b) => parseInt(a.year) - parseInt(b.year)); // Sort by year
    }
  }

  function handleImageError(filename) {
    imageErrors.add(filename);
    imageErrors = imageErrors; // Trigger reactivity
  }

  function handleImageLoad(filename) {
    composites = composites.map(comp => 
      comp.filename === filename ? { ...comp, loaded: true } : comp
    );
  }

  function goBack() {
    goto('/');
  }

  function downloadAll() {
    composites.forEach(({ year, filename }) => { console.log(tiffFilename);
      const tiffFilename = filename.replace('.png', '.tiff');
      const link = document.createElement('a');
      link.href = `http://localhost:8000/static/${tiffFilename}`;
      link.download = `satellite_${searchLocation}_${year}.tiff`;
      link.click();
    });
  }

  // Check if we have any images to display
  $: hasImages = composites.length > 0;
</script>

<svelte:head>
  <title>Satellite Images - {searchLocation}</title>
</svelte:head>

<main style="max-width: 1200px; margin: 2rem auto; font-family: sans-serif; padding: 0 1rem;">
  
  <!-- Header -->
  <header style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #1f2937; margin-bottom: 0.5rem;">
      🛰️ Satellite Images for {searchLocation}
    </h1>
    
    {#if optimalWindow}
      <p style="color: #6b7280; margin-bottom: 1rem;">
        <strong>Optimal Viewing Window:</strong> Month {optimalWindow.replace('-', ' to ')}
      </p>
    {/if}

    <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
      <button 
        on:click={goBack}
        style="padding: 0.5rem 1rem; background: #6b7280; color: white; border: none; border-radius: 5px; cursor: pointer;"
      >
        ← New Search
      </button>
      
      {#if hasImages}
        <button 
          on:click={downloadAll}
          style="padding: 0.5rem 1rem; background: #059669; color: white; border: none; border-radius: 5px; cursor: pointer;"
        >
          📥 Download All TIFF Files
        </button>
      {/if}
    </div>
  </header>

  {#if !hasImages}
    <!-- No Results -->
    <div style="text-align: center; padding: 3rem; background: #f9fafb; border-radius: 8px; border: 2px dashed #d1d5db;">
      <h3 style="color: #6b7280;">No satellite images found</h3>
      <p style="color: #9ca3af;">Try adjusting your search criteria or check a different location.</p>
    </div>
  {:else}
    <!-- Image Gallery -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-bottom: 2rem;">
      {#each composites as { year, filename, loaded }}
        <div style="background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
          
          <h3 style="color: #1f2937; margin-bottom: 1rem; font-size: 1.25rem;">
            📅 Year {year}
          </h3>

          <!-- Image with loading state -->
          <div style="position: relative; margin-bottom: 1rem;">
            {#if !loaded && !imageErrors.has(filename)}
              <div style="width: 256px; height: 256px; background: #f3f4f6; display: flex; align-items: center; justify-content: center; margin: 0 auto; border-radius: 8px;">
                <span style="color: #9ca3af;">Loading...</span>
              </div>
            {/if}

            {#if imageErrors.has(filename)}
              <div style="width: 256px; height: 256px; background: #fef2f2; border: 2px dashed #f87171; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 0 auto; border-radius: 8px; color: #dc2626;">
                <span>❌ Failed to load</span>
                <small>Image not available</small>
              </div>
            {:else}
              <img 
                src={`http://localhost:8000/${filename}`} 
                alt={`Satellite composite for ${searchLocation} in ${year}`}
                width="256"
                style="border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); {loaded ? '' : 'display: none;'}"
                on:load={() => handleImageLoad(filename)}
                on:error={() => handleImageError(filename)}
              />
            {/if}
          </div>

          <!-- Download Links -->
          <div style="display: flex; flex-direction: column; gap: 0.5rem;">
            <a 
              href={`http://localhost:8000/${filename}`} 
              target="_blank" 
              rel="noopener noreferrer"
              style="color: #3b82f6; text-decoration: none; font-weight: 500; padding: 0.5rem; border: 1px solid #3b82f6; border-radius: 5px; transition: all 0.2s;"
            >
              🖼️ View PNG
            </a>
            
            <a 
              href={`http://localhost:8000/${filename.replace('.png', '.tiff')}`} 
              target="_blank" 
              rel="noopener noreferrer"
              style="color: #059669; text-decoration: none; font-weight: 500; padding: 0.5rem; border: 1px solid #059669; border-radius: 5px; transition: all 0.2s;"
            >
              📁 Download TIFF
            </a>
          </div>
        </div>
      {/each}
    </div>

    <!-- Additional Info -->
    {#if skippedYears.length > 0}
      <div style="background: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 1rem; text-align: center;">
        <p style="color: #92400e; margin: 0;">
          <strong>⚠️ Note:</strong> No data available for years: {skippedYears.join(', ')}
        </p>
      </div>
    {/if}
  {/if}

</main>

<style>
  /* Hover effects for buttons and links */
  button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  a:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  img {
    transition: transform 0.2s ease;
  }

  img:hover {
    transform: scale(1.05);
  }
</style>