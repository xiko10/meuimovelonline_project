// ========================
// FUNÇÕES DO HEADER MENU
// ========================

function toggleMenu() {
  const menuButton = document.querySelector('.menu-button');
  const menuDropdown = document.getElementById('menuDropdown');
  const menuOverlay = document.getElementById('menuOverlay');
  
  const isActive = menuButton.classList.contains('active');
  
  if (isActive) {
    closeMenu();
  } else {
    openMenu();
  }
}

function openMenu() {
  const menuButton = document.querySelector('.menu-button');
  const menuDropdown = document.getElementById('menuDropdown');
  const menuOverlay = document.getElementById('menuOverlay');
  
  menuButton.classList.add('active');
  menuDropdown.classList.add('active');
  menuOverlay.classList.add('active');
}

function closeMenu() {
  const menuButton = document.querySelector('.menu-button');
  const menuDropdown = document.getElementById('menuDropdown');
  const menuOverlay = document.getElementById('menuOverlay');
  
  menuButton.classList.remove('active');
  menuDropdown.classList.remove('active');
  menuOverlay.classList.remove('active');
}

document.addEventListener('DOMContentLoaded', () => {
  // Elementos do carousel
  const carousel = document.querySelector('.carousel');
  const prevBtn = document.querySelector('.carousel-nav.prev');
  const nextBtn = document.querySelector('.carousel-nav.next');

  // Elementos do modal
  const modal = document.querySelector('.modal');
  const modalImg = modal.querySelector('.modal-content img');
  const modalCaption = modal.querySelector('.modal-caption');
  const modalCloseBtn = modal.querySelector('.modal-close');
  const modalPrevBtn = modal.querySelector('.modal-prev');
  const modalNextBtn = modal.querySelector('.modal-next');

  // Array de imagens e índice atual
  const images = Array.from(carousel.querySelectorAll('img'));
  let currentIndex = 0;

  // Navegação carrossel por botões
  const scrollAmount = () => {
    // scroll width of one image + margin
    const style = getComputedStyle(images[0]);
    const marginRight = parseInt(style.marginRight);
    return images[0].offsetWidth + marginRight;
  };

  if (prevBtn && nextBtn && carousel && images.length > 0) {
    prevBtn.addEventListener('click', () => {
      carousel.scrollBy({ left: -scrollAmount(), behavior: 'smooth' });
    });

    nextBtn.addEventListener('click', () => {
      carousel.scrollBy({ left: scrollAmount(), behavior: 'smooth' });
    });
  }


  // Abrir modal ao clicar na imagem
  images.forEach((img, index) => {
    img.addEventListener('click', () => {
      currentIndex = index;
      openModalGallery(); // Renomeada para evitar conflito
    });
  });

  function openModalGallery() { // Renomeada
    if (images.length === 0) return;
    const img = images[currentIndex];
    modalImg.src = img.src;
    modalImg.alt = img.alt;
    modalCaption.textContent = img.alt || '';
    modal.classList.remove('hidden');
    modal.focus();
  }

  // Fechar modal
  if (modalCloseBtn && modal && modalImg && modalCaption) {
    modalCloseBtn.addEventListener('click', closeModalGallery);
    modal.addEventListener('click', e => {
      if (e.target === modal) closeModalGallery();
    });
  }


  function closeModalGallery() {
    modal.classList.add('hidden');
    modalImg.src = ''; // Limpar para não mostrar imagem antiga piscando
    modalCaption.textContent = '';
  }

  // Navegação modal
  if (modalPrevBtn && modalNextBtn && images.length > 0) {
    modalPrevBtn.addEventListener('click', () => {
      currentIndex = (currentIndex - 1 + images.length) % images.length;
      openModalGallery();
    });

    modalNextBtn.addEventListener('click', () => {
      currentIndex = (currentIndex + 1) % images.length;
      openModalGallery();
    });
  }


  // Navegação teclado modal (esc, setas)
  document.addEventListener('keydown', e => {
    if (modal && !modal.classList.contains('hidden')) {
      if (e.key === 'Escape') {
        closeModalGallery();
      } else if (e.key === 'ArrowLeft' && images.length > 0) {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        openModalGallery();
      } else if (e.key === 'ArrowRight' && images.length > 0) {
        currentIndex = (currentIndex + 1) % images.length;
        openModalGallery();
      }
    }
  });

    // ========================
  // FUNCIONALIDADE DOS MODAIS DE MÍDIAS
  // ========================
  const mediaButtons = document.querySelectorAll('.btn-midia');
  const mediaModal = document.getElementById('mediaModal');
  const mediaModalContentBody = mediaModal ? mediaModal.querySelector('.modal-midia-body') : null;
  const mediaModalTitle = mediaModal ? mediaModal.querySelector('.modal-midia-title') : null;
  const mediaModalCloseBtn = mediaModal ? mediaModal.querySelector('.modal-midia-close') : null;

  if (mediaButtons.length > 0 && mediaModal && mediaModalContentBody && mediaModalTitle && mediaModalCloseBtn) {
    mediaButtons.forEach(button => {
      button.addEventListener('click', () => {
        const modalType = button.dataset.modalType;
        let contentHtml = '';
        let titleText = '';

        switch (modalType) {
          case 'fotos':
            titleText = 'Galeria de Fotos';
            contentHtml = '<p>Aqui você verá a galeria de fotos do empreendimento.</p><img src="https://via.placeholder.com/600x400/cccccc/888888?text=Placeholder+Foto" alt="Placeholder Foto">';
            break;
          case 'video':
            titleText = 'Vídeo de Apresentação';
            contentHtml = '<p>Assista ao vídeo completo.</p><iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
            break;
          case 'localizacao':
            titleText = 'Localização no Mapa';
            contentHtml = '<p>Veja a localização privilegiada.</p><img src="https://via.placeholder.com/600x400/A9D4A9/004132?text=Placeholder+Mapa" alt="Placeholder Mapa">';
            break;
          case 'revista':
            titleText = 'Revista Digital';
            contentHtml = '<p>Acesse nossa revista digital com todos os detalhes.</p><img src="https://via.placeholder.com/600x400/FFDDC1/D95F0E?text=Placeholder+Revista" alt="Placeholder Revista">';
            break;
          case 'ficha':
            titleText = 'Ficha Técnica';
            contentHtml = '<h3>Detalhes do Empreendimento</h3><ul><li>Característica 1</li><li>Característica 2</li><li>Planta baixa, etc.</li></ul>';
            break;
          default:
            titleText = 'Informações';
            contentHtml = '<p>Conteúdo não especificado.</p>';
        }

        mediaModalTitle.textContent = titleText;
        mediaModalContentBody.innerHTML = contentHtml;
        mediaModal.classList.remove('hidden');
      });
    });

    mediaModalCloseBtn.addEventListener('click', () => {
      mediaModal.classList.add('hidden');
      mediaModalContentBody.innerHTML = ''; // Limpa o conteúdo para iframes pararem de tocar, etc.
    });

    mediaModal.addEventListener('click', (event) => {
      if (event.target === mediaModal) {
        mediaModal.classList.add('hidden');
        mediaModalContentBody.innerHTML = ''; // Limpa o conteúdo
      }
    });
  } else {
    console.warn('Elementos para os modais de mídias não foram completamente encontrados. Funcionalidade pode estar comprometida.');
  }
  
  // ========================
  // FUNCIONALIDADE SEÇÃO TIPOS & UNIDADES
  // ========================
  const carrosselTiposUnidades = document.querySelector('.tipos-unidades-carrossel');
  const cardsUnidade = document.querySelectorAll('.card-unidade'); // Movido para cima para uso na nova funcionalidade
  const navPrevTiposUnidades = document.querySelector('.tipos-unidades-nav-prev');
  const navNextTiposUnidades = document.querySelector('.tipos-unidades-nav-next');

  if (cardsUnidade.length > 0) {
    cardsUnidade.forEach(card => {
      card.addEventListener('click', () => {
        cardsUnidade.forEach(c => {
            c.classList.remove('selected');
            c.setAttribute('aria-pressed', 'false');
        });
        card.classList.add('selected');
        card.setAttribute('aria-pressed', 'true');
        // A nova funcionalidade de atualização de plantas será chamada aqui
      });
      card.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault(); 
          card.click(); 
        }
      });
    });
  }

  if (carrosselTiposUnidades && navPrevTiposUnidades && navNextTiposUnidades) {
    const scrollAmountCards = () => {
        if (cardsUnidade.length > 0) {
            const cardStyle = getComputedStyle(cardsUnidade[0]);
            const cardWidth = cardsUnidade[0].offsetWidth;
            // Usa o gap definido no CSS se possível, ou um fallback.
            const gapValue = cardStyle.gap ? parseInt(cardStyle.gap) : (parseInt(cardStyle.marginLeft) + parseInt(cardStyle.marginRight));
            const gap = isNaN(gapValue) ? 20 : gapValue; // Fallback para o gap
            return cardWidth + gap; 
        }
        return 250; 
    };

    navPrevTiposUnidades.addEventListener('click', () => {
      carrosselTiposUnidades.scrollBy({ left: -scrollAmountCards(), behavior: 'smooth' });
    });

    navNextTiposUnidades.addEventListener('click', () => {
      carrosselTiposUnidades.scrollBy({ left: scrollAmountCards(), behavior: 'smooth' });
    });
  } else {
      if(navPrevTiposUnidades) navPrevTiposUnidades.style.display = 'none';
      if(navNextTiposUnidades) navNextTiposUnidades.style.display = 'none';
  }

   // ==================================================
  // FUNCIONALIDADE DE ARRASTAR PARA ROLAR (DRAG-TO-SCROLL)
  // PARA O CARROSSEL DE TIPOS & UNIDADES (DESKTOP)
  // ==================================================
  const sliderTiposUnidades = document.querySelector('.tipos-unidades-carrossel');

  if (sliderTiposUnidades) {
    let isDown = false; 
    let startX;         
    let scrollLeft;     

    sliderTiposUnidades.addEventListener('mousedown', (e) => {
      isDown = true;
      sliderTiposUnidades.classList.add('dragging'); 
      startX = e.pageX - sliderTiposUnidades.offsetLeft; 
      scrollLeft = sliderTiposUnidades.scrollLeft;      
    });

    sliderTiposUnidades.addEventListener('mouseleave', () => {
      isDown = false;
      sliderTiposUnidades.classList.remove('dragging');
    });

    sliderTiposUnidades.addEventListener('mouseup', () => {
      isDown = false;
      sliderTiposUnidades.classList.remove('dragging');
    });

    sliderTiposUnidades.addEventListener('mousemove', (e) => {
      if (!isDown) return; 
      e.preventDefault();   
      const x = e.pageX - sliderTiposUnidades.offsetLeft;
      const walk = (x - startX) * 2; 
      sliderTiposUnidades.scrollLeft = scrollLeft - walk; 
    });
  }

    // =================================
  // FUNCIONALIDADE MODAL IMAGEM PLANTA
  // =================================
  const imagemPlantaTrigger = document.getElementById('imagemPlantaModalTrigger');
  const modalPlanta = document.getElementById('modalPlanta');
  const modalPlantaCloseBtn = modalPlanta ? modalPlanta.querySelector('.modal-planta-close') : null;

  if (imagemPlantaTrigger && modalPlanta && modalPlantaCloseBtn) {
    imagemPlantaTrigger.addEventListener('click', () => {
      modalPlanta.classList.remove('hidden');
    });

    function fecharModalPlanta() {
      modalPlanta.classList.add('hidden');
    }

    modalPlantaCloseBtn.addEventListener('click', fecharModalPlanta);

    modalPlanta.addEventListener('click', (event) => {
      if (event.target === modalPlanta) { 
        fecharModalPlanta();
      }
    });
  } else {
    console.warn('Elementos para o modal da planta não foram completamente encontrados.');
  }

  // ============================================================
  // NOVA FUNCIONALIDADE: ATUALIZAR SEÇÃO PLANTAS AO CLICAR NO CARD
  // ============================================================

  // 1. Estrutura de dados das unidades
  //    (Você precisará preencher com os dados reais e imagens corretas)
  const unidadesData = [
    {
      id: 'apt30', // Deve corresponder ao data-id no HTML do card
      nomeUnidade: 'Apartamento 30m²',
      imagemPlantaTriggerSrc: 'img/planta_1.png',
      imagemPlantaTriggerAlt: 'Planta do Apartamento 30m²',
      imagemPlantaModalSrc: 'img/planta_1.png',
      imagemPlantaModalAlt: 'Planta Ampliada do Apartamento 30m²',
      valores: {
        entrada: 'R$ 29.500,00',
        sinal: 'R$ 15.000,00',
        parcelaMensal: 'R$ 1.800,00',
        balaoAnual: 'R$ 10.000,00',
        financiamento: 'R$ 150.700,00'
      }
    },
    {
      id: 'apt45', // Exemplo de uma segunda unidade
      nomeUnidade: 'Apartamento 45m²',
      imagemPlantaTriggerSrc: 'https://via.placeholder.com/600x700/FFCCAA/000000?text=Planta+45m%C2%B2',
      imagemPlantaTriggerAlt: 'Planta do Apartamento 45m²',
      imagemPlantaModalSrc: 'https://via.placeholder.com/800x1000/FFCCAA/000000?text=Planta+Ampliada+45m%C2%B2',
      imagemPlantaModalAlt: 'Planta Ampliada do Apartamento 45m²',
      valores: {
        entrada: 'R$ 43.000,00',
        sinal: 'R$ 22.000,00',
        parcelaMensal: 'R$ 2.200,00',
        balaoAnual: 'R$ 18.000,00',
        financiamento: 'R$ 220.500,00'
      }
    },
    {
      id: 'apt60', // Exemplo de uma terceira unidade
      nomeUnidade: 'Apartamento 60m²',
      imagemPlantaTriggerSrc: 'https://via.placeholder.com/600x700/AAFFAA/000000?text=Planta+60m%C2%B2',
      imagemPlantaTriggerAlt: 'Planta do Apartamento 60m²',
      imagemPlantaModalSrc: 'https://via.placeholder.com/800x1000/AAFFAA/000000?text=Planta+Ampliada+60m%C2%B2',
      imagemPlantaModalAlt: 'Planta Ampliada do Apartamento 60m²',
      valores: {
        entrada: 'R$ 65.000,00',
        sinal: 'R$ 30.000,00',
        parcelaMensal: 'R$ 3.100,00',
        balaoAnual: 'R$ 25.000,00',
        financiamento: 'R$ 295.300,00'
      }
    }
    // Adicione mais objetos de unidade conforme necessário
  ];

  // 2. Função para atualizar as informações da seção de plantas
  function updatePlantasInfo(unitId) {
    const unitData = unidadesData.find(unit => unit.id === unitId);
    if (!unitData) {
      console.warn(`Dados da unidade não encontrados para o ID: ${unitId}`);
      // Opcional: Limpar campos ou mostrar mensagem de erro
      // Limpar campos para evitar mostrar dados de unidade anterior:
      const imagemPlantaTriggerEl = document.getElementById('imagemPlantaModalTrigger');
      if (imagemPlantaTriggerEl) {
        imagemPlantaTriggerEl.src = 'https://via.placeholder.com/600x700/cccccc/888888?text=Planta+Indispon%C3%ADvel';
        imagemPlantaTriggerEl.alt = 'Planta do Imóvel Indisponível';
      }
      const imagemModalPlantaAmpliadaEl = document.getElementById('imagemModalPlantaAmpliada');
      if (imagemModalPlantaAmpliadaEl) {
        imagemModalPlantaAmpliadaEl.src = 'https://via.placeholder.com/800x1000/cccccc/888888?text=Planta+Ampliada+Indispon%C3%ADvel';
        imagemModalPlantaAmpliadaEl.alt = 'Planta do Imóvel Ampliada Indisponível';
      }
      const valorDefault = '---';
      if(document.getElementById('valorEntrada')) document.getElementById('valorEntrada').textContent = valorDefault;
      if(document.getElementById('valorSinal')) document.getElementById('valorSinal').textContent = valorDefault;
      if(document.getElementById('valorParcelaMensal')) document.getElementById('valorParcelaMensal').textContent = valorDefault;
      if(document.getElementById('valorBalaoAnual')) document.getElementById('valorBalaoAnual').textContent = valorDefault;
      if(document.getElementById('valorFinanciamento')) document.getElementById('valorFinanciamento').textContent = valorDefault;
      return;
    }

    // Atualizar imagem da planta principal (que também é o trigger do modal)
    const imagemPlantaTriggerEl = document.getElementById('imagemPlantaModalTrigger');
    if (imagemPlantaTriggerEl) {
      imagemPlantaTriggerEl.src = unitData.imagemPlantaTriggerSrc;
      imagemPlantaTriggerEl.alt = unitData.imagemPlantaTriggerAlt;
    } else {
      console.warn("Elemento 'imagemPlantaModalTrigger' não encontrado.");
    }

    // Atualizar imagem da planta no modal
    const imagemModalPlantaAmpliadaEl = document.getElementById('imagemModalPlantaAmpliada');
    if (imagemModalPlantaAmpliadaEl) {
      imagemModalPlantaAmpliadaEl.src = unitData.imagemPlantaModalSrc;
      imagemModalPlantaAmpliadaEl.alt = unitData.imagemPlantaModalAlt;
    } else {
      console.warn("Elemento 'imagemModalPlantaAmpliada' não encontrado.");
    }

    // Atualizar valores financeiros
    // Certifique-se de que os IDs no HTML correspondem exatamente
    if(document.getElementById('valorEntrada')) document.getElementById('valorEntrada').textContent = unitData.valores.entrada;
    if(document.getElementById('valorSinal')) document.getElementById('valorSinal').textContent = unitData.valores.sinal;
    if(document.getElementById('valorParcelaMensal')) document.getElementById('valorParcelaMensal').textContent = unitData.valores.parcelaMensal;
    if(document.getElementById('valorBalaoAnual')) document.getElementById('valorBalaoAnual').textContent = unitData.valores.balaoAnual;
    if(document.getElementById('valorFinanciamento')) document.getElementById('valorFinanciamento').textContent = unitData.valores.financiamento;
  }

  // 3. Adicionar event listeners aos cards de unidade
  if (cardsUnidade.length > 0) {
    cardsUnidade.forEach(card => {
      // O listener de clique já existe acima para a seleção do card (classe 'selected').
      // Apenas adicionamos a chamada para atualizar as informações.
      card.addEventListener('click', () => {
        const unitId = card.dataset.id;
        if (unitId) {
          updatePlantasInfo(unitId);
        } else {
          console.warn('Card de unidade não possui data-id.');
        }
      });
    });

    // 4. Atualizar informações para o card inicialmente selecionado (se houver)
    const selectedCard = document.querySelector('.card-unidade.selected');
    if (selectedCard) {
      const initialUnitId = selectedCard.dataset.id;
      if (initialUnitId) {
        updatePlantasInfo(initialUnitId);
      }
    } else if (cardsUnidade.length > 0 && cardsUnidade[0].dataset.id) {
        // Ou carrega o primeiro card se nenhum estiver selecionado, mas existe um ID
        updatePlantasInfo(cardsUnidade[0].dataset.id);
    }
  }
  // FIM DA NOVA FUNCIONALIDADE
  // ============================================================


  // ========================
  // EVENT LISTENERS GLOBAIS (Já existentes, podem precisar de ajustes se houver sobreposição)
  // ========================

  // Fechar menus e modais com ESC
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
      // Menu principal
      if (document.getElementById('menuDropdown') && document.getElementById('menuDropdown').classList.contains('active')) {
        closeMenu();
      }
      // Modal da galeria de imagens
      if (modal && !modal.classList.contains('hidden')) {
        closeModalGallery();
      }
      // Modal de mídias
      if (mediaModal && !mediaModal.classList.contains('hidden')) {
        mediaModal.classList.add('hidden');
        if(mediaModalContentBody) mediaModalContentBody.innerHTML = ''; // Limpa o conteúdo
      }
      // Modal da planta
      if (modalPlanta && !modalPlanta.classList.contains('hidden')) {
        const fecharModalPlantaFunc = modalPlantaCloseBtn?.onclick || (() => modalPlanta.classList.add('hidden'));
        fecharModalPlantaFunc();
      }
    }
  });

  // Fechar menu ao clicar em um link
  document.querySelectorAll('.menu-dropdown a').forEach(link => {
    link.addEventListener('click', closeMenu);
  });
});