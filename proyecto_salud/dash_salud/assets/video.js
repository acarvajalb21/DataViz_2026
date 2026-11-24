// Sección Video, común a Dash y Shiny: paradas que llevan a cada parte y portada propia.
(function () {
  "use strict";
  function marco(nodo) { return nodo && nodo.closest ? nodo.closest(".video-banda") : null; }

  // Con preload="none" la posición solo se puede fijar cuando llegan los metadatos.
  function irA(video, segundo) {
    function mover() {
      video.currentTime = segundo;
      var inicio = video.play();
      if (inicio && inicio.catch) inicio.catch(function () {});
    }
    if (video.readyState >= 1) return mover();
    // Si se pulsan varias paradas antes de cargar, vale la última.
    if (video._alCargar) video.removeEventListener("loadedmetadata", video._alCargar);
    video._alCargar = mover;
    video.addEventListener("loadedmetadata", mover, { once: true });
    video.load();
  }

  // Al cambiar de sección el video queda oculto: se pausa para que no siga sonando.
  function pausarOculto(video) { if (!video.getClientRects().length && !video.paused) video.pause(); }

  function marcar(video) {
    var paradas = marco(video).querySelectorAll(".video-parada");
    var actual = -1;
    paradas.forEach(function (p, i) { if (video.currentTime + .25 >= Number(p.getAttribute("data-video-ir"))) actual = i; });
    paradas.forEach(function (p, i) {
      p.classList.toggle("recorrida", i < actual);
      if (i === actual) p.setAttribute("aria-current", "true"); else p.removeAttribute("aria-current");
    });
  }

  document.addEventListener("click", function (e) {
    var boton = e.target.closest ? e.target.closest("[data-video-ir]") : null;
    var banda = marco(boton);
    var video = banda && banda.querySelector("video");
    if (!video) return;
    irA(video, Number(boton.getAttribute("data-video-ir")));
    if (boton.classList.contains("video-reproducir")) video.focus();
    else if (window.matchMedia("(max-width: 960px)").matches) video.scrollIntoView({ block: "center" });
  });

  // Los eventos de reproducción no suben por el documento: se escuchan en la captura.
  document.addEventListener("play", function (e) {
    var banda = marco(e.target);
    if (banda) { banda.classList.add("iniciado"); marcar(e.target); }
  }, true);
  ["timeupdate", "seeked"].forEach(function (evento) {
    document.addEventListener(evento, function (e) {
      var banda = marco(e.target);
      if (!banda || !banda.classList.contains("iniciado")) return;
      pausarOculto(e.target);
      marcar(e.target);
    }, true);
  });
  document.addEventListener("error", function (e) {
    var banda = marco(e.target);
    if (banda && e.target.tagName === "VIDEO") banda.classList.add("con-error");
  }, true);

  var vistos = new WeakSet();
  function observar() {
    document.querySelectorAll(".video-banda video").forEach(function (video) {
      if (vistos.has(video) || !window.ResizeObserver) return;
      vistos.add(video);
      video.setAttribute("playsinline", "");
      new ResizeObserver(function () { pausarOculto(video); }).observe(video);
    });
  }
  new MutationObserver(observar).observe(document.documentElement, { childList: true, subtree: true });
  observar();
})();
