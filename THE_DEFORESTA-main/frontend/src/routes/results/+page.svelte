// Results Page (results/+page.svelte)
<script>
  import { page } from '$app/stores';
//   import { analyzeSatelliteImages } from '../lib/satellite-analyzer.js';
// adjust path as needed, for example: '../../lib/satellite-analyzer.js'

// Adjust the path as needed

  let composites = [];
  let searchLocation = '';
  let optimalWindow = '';
  let skippedYears = [];
  let loading = false;
  let imageErrors = new Set();
  let image_paths = [];
  
  // Chat functionality
  let chatMessages = [];
  let currentMessage = '';
  let chatLoading = false;
  let isChatOpen = false;

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
    composites.forEach(({ year, filename }) => {
      const tiffFilename = filename.replace('.png', '.tiff');
      const link = document.createElement('a');
      link.href = `http://localhost:8000/output/${tiffFilename}`;
      link.download = `satellite_${searchLocation}_${year}.tiff`;
      link.click();
    });
  }

  // Check if we have any images to display
  $: hasImages = composites.length > 0;

  // Chat functions
  async function sendMessage() {
    if (!currentMessage.trim() || chatLoading) return;

    const userMessage = currentMessage.trim();
    currentMessage = '';
    
    // Add user message to chat
    chatMessages = [...chatMessages, {
      type: 'user',
      content: userMessage,

      timestamp: new Date()

    }];
    console.log(userMessage);


   

    chatLoading = true;

    try {
      // Prepare context about the satellite images
      const imageContext = {
        location: searchLocation,
        years: composites.map(c => c.year),
        optimalWindow: optimalWindow,
        skippedYears: skippedYears,
        totalImages: composites.length
      };

      for(const img of composites) {
        console.log("Image:", img.filename);
        image_paths.push(img.filename);
      }

      print("Sending chat request with context:", );

      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: userMessage,
          images: image_paths,
          context: imageContext
        })
      });


      const data = await response.json();


      
      if (response.ok) {
        console.log("Chat response:", data);
        chatMessages = [...chatMessages, {
          type: 'bot',
          content: data.message || 'Sorry, I could not process your request.',
          timestamp: new Date()
        }];
      } else {
        throw new Error(data.error || 'Chat service error');
      }
    } catch (error) {
      console.error('Chat error:', error);
      chatMessages = [...chatMessages, {
        type: 'bot',
        content: 'Sorry, I encountered an error while processing your message. Please try again.',
        timestamp: new Date()
      }];
    } finally {
      chatLoading = false;
    }
  }

  function toggleChat(e) { console.log(e);
    isChatOpen = !isChatOpen;
    if (isChatOpen && chatMessages.length === 0) {
      // Add welcome message
      chatMessages = [{
        type: 'bot',
        content: `Hello! I'm here to help you analyze the satellite images for ${searchLocation}. You can ask me about changes over time, patterns, or any observations about these images.`,
        timestamp: new Date()
      }];   
    }
  }

  function clearChat() {
    chatMessages = [];
  }
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

        <button 
          on:click={toggleChat}
          style="padding: 0.5rem 1rem; background: {isChatOpen ? '#dc2626' : '#3b82f6'}; color: white; border: none; border-radius: 5px; cursor: pointer;"
        >
          {isChatOpen ? '❌ Close Chat' : '💬 Chat with AI'}
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

  <!-- Chatbot Interface -->
  {#if isChatOpen && hasImages}
    <div style="position: fixed; bottom: 2rem; right: 2rem; width: 400px; max-width: 90vw; background: white; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.2); z-index: 1000; max-height: 600px; display: flex; flex-direction: column;">
      
      <!-- Chat Header -->
      <div style="padding: 1rem; border-bottom: 1px solid #e5e7eb; background: #3b82f6; color: white; border-radius: 12px 12px 0 0; display: flex; justify-content: space-between; align-items: center;">
        <h3 style="margin: 0; font-size: 1rem;">🤖 Satellite Image Assistant</h3>
        <div>
          <button 
            on:click={clearChat}
            style="background: none; border: none; color: white; cursor: pointer; padding: 0.25rem; margin-right: 0.5rem; opacity: 0.8;"
            title="Clear chat"
          >
            🗑️
          </button>
          <button 
            on:click={toggleChat}
            style="background: none; border: none; color: white; cursor: pointer; padding: 0.25rem; opacity: 0.8;"
            title="Close chat"
          >
            ❌
          </button>
        </div>
      </div>

      <!-- Chat Messages -->
      <div style="flex: 1; padding: 1rem; overflow-y: auto; max-height: 400px; min-height: 200px;">
        {#each chatMessages as message}
          <div style="margin-bottom: 1rem; display: flex; {message.type === 'user' ? 'justify-content: flex-end' : 'justify-content: flex-start'};">
            <div style="max-width: 80%; padding: 0.75rem; border-radius: 8px; {message.type === 'user' ? 'background: #3b82f6; color: white;' : 'background: #f3f4f6; color: #1f2937;'}">
              <div style="font-size: 0.875rem; line-height: 1.4;">
                {message.content}
              </div>
              <div style="font-size: 0.75rem; opacity: 0.7; margin-top: 0.25rem;">
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          </div>
        {/each}

        {#if chatLoading}
          <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
            <div style="background: #f3f4f6; padding: 0.75rem; border-radius: 8px;">
              <div style="color: #6b7280; font-size: 0.875rem;">
                🤔 Analyzing images...
              </div>
            </div>
          </div>
        {/if}
      </div>

      <!-- Chat Input -->
      <div style="padding: 1rem; border-top: 1px solid #e5e7eb;">
        <form on:submit|preventDefault={sendMessage} style="display: flex; gap: 0.5rem;">
          <input 
            bind:value={currentMessage}
            placeholder="Ask about the satellite images..."
            disabled={chatLoading}
            style="flex: 1; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.875rem;"
          />
          <button 
            type="submit" 
            disabled={!currentMessage.trim() || chatLoading}
            style="padding: 0.5rem 1rem; background: {currentMessage.trim() && !chatLoading ? '#3b82f6' : '#9ca3af'}; color: white; border: none; border-radius: 6px; cursor: {currentMessage.trim() && !chatLoading ? 'pointer' : 'not-allowed'}; font-size: 0.875rem;"
          >
            {chatLoading ? '⏳' : '➤'}
          </button>
        </form>
        
        <!-- Quick Questions -->
        <div style="margin-top: 0.5rem; display: flex; flex-wrap: wrap; gap: 0.25rem;">
          {#each ['Show changes over time', 'Analyze vegetation', 'Detect urban growth', 'Compare years'] as suggestion}
            <button 
              on:click={() => { currentMessage = suggestion; sendMessage(); }}
              disabled={chatLoading}
              style="font-size: 0.75rem; padding: 0.25rem 0.5rem; background: #f3f4f6; border: 1px solid #d1d5db; border-radius: 4px; cursor: pointer; color: #6b7280;"
            >
              {suggestion}
            </button>
          {/each}
        </div>
      </div>
    </div>
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