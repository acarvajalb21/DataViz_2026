# Biblioteca compartida por RStudio y los iniciadores de este proyecto.
if (.Platform$OS.type == "windows") {
  invisible(try(Sys.setlocale("LC_CTYPE", "English_United States.utf8"), silent = TRUE))
}
local({
  project_root <- getwd()
  while (!file.exists(file.path(project_root, "DataViz_2026.Rproj"))) {
    parent <- dirname(project_root)
    if (identical(parent, project_root)) break
    project_root <- parent
  }
  project_lib <- file.path(project_root, ".dataviz-runtime", "r-library")
  if (dir.exists(project_lib)) {
    project_lib <- normalizePath(project_lib, winslash = "/")
    Sys.setenv(R_LIBS_USER = project_lib)
    .libPaths(c(project_lib, .libPaths()))
  }
})
