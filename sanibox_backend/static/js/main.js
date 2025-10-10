    // ===== main.js (embedded) =====

    // Mock trending posters — replace with real images
    const posters = [
      'images/posters/anime1.jpg','images/posters/anime2.jpg','images/posters/anime3.jpg','images/posters/anime4.jpg','images/posters/anime5.jpg','images/posters/anime6.jpg','images/posters/anime7.jpg'
    ]

    const trending = document.getElementById('trending')
    trending.innerHTML = posters.map(p=>`
      <div class="card" style="position:relative">
        <img src="${p}" alt="poster"/>
        <div class="meta">
          <div class="title">${p.split('/').pop().replace('.jpg','').replace('anime','Anime ')}</div>
          <div class="sub">Latest • EP 12</div>
        </div>
      </div>
    `).join('')

    // Initialize Swiper (options: autoplay, fade effect, nav)
    const swiper = new Swiper('.mySwiper', {
      modules: [Swiper.Navigation, Swiper.Pagination, Swiper.Autoplay, Swiper.EffectFade],
      effect: 'fade',
      speed: 700,
      loop: true,
      autoplay: { delay: 4500, disableOnInteraction: false },
      pagination: { el: '.swiper-pagination', clickable: true },
      navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
    })

    // Modal functions
    function openTrailer(id){
      const titles = ['Blade of Dawn','Falling Stars','Tokyo Raid']
      document.getElementById('modalTitle').innerText = titles[id-1] + ' — Trailer'
      document.getElementById('modalBody').innerHTML = `
        <div style="position:relative;padding-top:56.25%">
          <!-- Replace iframe src with real trailer URL -->
          <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1" style="position:absolute;inset:0;border:0;width:100%;height:100%" allowfullscreen allow="autoplay"></iframe>
        </div>`
      document.getElementById('modalBackdrop').style.display = 'flex'
    }
    function closeModal(){ document.getElementById('modalBackdrop').style.display = 'none'; document.getElementById('modalBody').innerHTML = '<div style="background:#000;border-radius:8px;padding:12px;color:var(--muted);min-height:200px">Trailer player placeholder (replace with your video embed)</div>' }

    // Accessibility: ESC to close
    document.addEventListener('keydown', (e)=>{ if(e.key==='Escape') closeModal() })