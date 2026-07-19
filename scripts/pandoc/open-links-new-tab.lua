-- Pandoc Lua filter: make every link in the HTML output open in a new
-- tab, applied uniformly to internal chapter links and external citation
-- links alike. Same-page anchor fragments (e.g. "#some-heading", used by
-- Pandoc's own table of contents) are left alone, since "open in a new
-- tab" makes no sense for a link that just scrolls the current page.
--
-- Used only for HTML builds (see scripts/bash/build-book.sh); EPUB output
-- does not use this filter, since e-readers have no tab concept and
-- rewriting internal navigation with target="_blank" there would be
-- meaningless at best.
function Link(el)
  if el.target:match("^#") then
    return el
  end
  el.attributes["target"] = "_blank"
  el.attributes["rel"] = "noopener noreferrer"
  return el
end
