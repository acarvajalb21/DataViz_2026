# Sirve el video por trozos. Las rutas estáticas de httpuv no admiten rangos, y sin
# ellos el navegador no puede saltar a una parte ni reproducirlo en Safari.

RUTA_VIDEO <- normalizePath("media/presentacion.mp4", mustWork = FALSE)
TROZO_VIDEO <- 2 * 1024^2

# Límites pedidos, en bytes desde cero y con el último incluido; NULL si no se pueden atender.
rango_video <- function(cabecera, tamano) {
  partes <- regmatches(cabecera, regexec("^bytes=([0-9]*)-([0-9]*)$", trimws(cabecera)))[[1]]
  if (length(partes) != 3 || all(partes[2:3] == "")) return(NULL)
  desde <- as.numeric(partes[2])
  hasta <- as.numeric(partes[3])
  if (is.na(desde)) {
    desde <- max(0, tamano - hasta)
    hasta <- tamano - 1
  }
  if (is.na(hasta)) hasta <- tamano - 1
  if (desde >= tamano || hasta < desde) return(NULL)
  c(desde, min(hasta, tamano - 1, desde + TROZO_VIDEO - 1))
}

responder_video <- function(req) {
  if (!identical(req$PATH_INFO, "/video/presentacion.mp4") || !file.exists(RUTA_VIDEO)) {
    return(httpResponse(404L, "text/plain; charset=UTF-8", "No se encontró el video."))
  }
  tamano <- file.size(RUTA_VIDEO)
  cabeceras <- list(`Accept-Ranges` = "bytes", `Cache-Control` = "public, max-age=86400")
  if (is.null(req$HTTP_RANGE)) {
    return(httpResponse(200L, "video/mp4", readBin(RUTA_VIDEO, "raw", tamano), cabeceras))
  }
  limites <- rango_video(req$HTTP_RANGE, tamano)
  if (is.null(limites)) {
    cabeceras[["Content-Range"]] <- sprintf("bytes */%.0f", tamano)
    return(httpResponse(416L, "video/mp4", raw(0), cabeceras))
  }
  archivo <- file(RUTA_VIDEO, "rb")
  on.exit(close(archivo))
  seek(archivo, limites[1])
  cabeceras[["Content-Range"]] <- sprintf("bytes %.0f-%.0f/%.0f", limites[1], limites[2], tamano)
  httpResponse(206L, "video/mp4", readBin(archivo, "raw", limites[2] - limites[1] + 1), cabeceras)
}
