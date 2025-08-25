// Search Page (SatelliteImageFinder.svelte)
<script>
  import { goto } from '$app/navigation';
  
  let place = "";
  let startYear = "2023";
  let endYear = "2025";
  let loading = false;
  let results = null;
  let error = "";

  async function getImages() {
    loading = true;
    error = "";
    results = null;

    const params = new URLSearchParams({
      place,
      start_year: startYear,
      end_year: endYear
    });

    try {
      const res = await fetch(`http://localhost:8000/generate_yearly_composites?${params.toString()}`);
      const data = await res.json();

      if (!res.ok) {
        error = data.error || "Backend error. Try a different place or years!";
        return;
      }

      results = data.results;
      
      // Check if we have valid results
      if (!results?.composites || Object.keys(results.composites).length === 0) {
        error = "No satellite images found for the specified criteria.";
        return;
      }

      // Prepare image parameters for URL
      const imagesParam = Object.entries(results.composites)
        .map(([year, path]) => {
          const pngFilename = path.replace('.tiff', '.png').split('/').pop();
          return `${year}|${pngFilename}`;
        })
        .join(',');

      // Navigate to results page with additional metadata
      const urlParams = new URLSearchParams({
        images: imagesParam,
        place: place,
        optimal_window: `${results.optimal_window_months?.[0]}-${results.optimal_window_months?.[1]}`,
        skipped_years: results.skipped_years?.join(',') || ''
      });

      goto(`/results?${urlParams.toString()}`);

    } catch (e) {
      console.error('Error fetching images:', e);
      error = "Could not connect to backend. Is the backend running?";
    } finally {
      loading = false;
    }
  }

  // Form validation
  $: isValidRange = parseInt(endYear) >= parseInt(startYear);
  $: canSubmit = place.trim() && isValidRange && !loading;
</script>

<main style="max-width: 500px; margin: 2rem auto; font-family: sans-serif; background: #f8fafc; border-radius: 12px; padding: 2rem; box-shadow: 0 2px 16px #d0e2f2;">
  <h2 style="text-align: center; color: #3a5a40;">Satellite Image Finder</h2>
  
  <form on:submit|preventDefault={getImages}>
    <label>
      🌍 <span style="font-weight: bold;">City or Country</span>:
      <input 
        type="text" 
        bind:value={place} 
        placeholder="e.g. Pune, India" 
        required 
        style="margin: 0.5rem 0; padding: 0.5rem; width: 100%; border-radius: 5px; border: 1px solid #ccc;" 
      />
    </label>
    <br />
    
    <div style="display: flex; gap: 1rem; margin: 1rem 0;">
      <label style="flex: 1;">
        Start Year:
        <input 
          type="number" 
          bind:value={startYear} 
          min="2000" 
          max="2024" 
          required 
          style="width: 100%; padding: 0.5rem; border-radius: 5px; border: 1px solid #ccc;"
        />
      </label>
      
      <label style="flex: 1;">
        End Year:
        <input 
          type="number" 
          bind:value={endYear} 
          min="2000" 
          max="2024" 
          required 
          style="width: 100%; padding: 0.5rem; border-radius: 5px; border: 1px solid #ccc;"
        />
      </label>
    </div>

    {#if !isValidRange}
      <p style="color: #d97706; font-size: 0.875rem;">End year must be greater than or equal to start year.</p>
    {/if}
    
    <button 
      type="submit" 
      disabled={!canSubmit}
      style="padding: 0.7rem 1.5rem; background: {canSubmit ? '#3a5a40' : '#9ca3af'}; color: white; border: none; border-radius: 5px; font-weight: bold; width: 100%; cursor: {canSubmit ? 'pointer' : 'not-allowed'};"
    >
      {loading ? "🔍 Searching..." : "Find Satellite Images"}
    </button>
  </form>

  {#if error}
    <div style="color: #dc2626; background: #fef2f2; border: 1px solid #fecaca; border-radius: 5px; padding: 1rem; margin-top: 1rem;">
      <strong>Error:</strong> {error}
    </div>
  {/if}
</main>