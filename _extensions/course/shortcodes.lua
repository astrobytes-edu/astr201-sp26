-- Course-specific shortcodes for ASTR 201
-- Usage: {{< shortcode arg1 arg2 >}}

-- {{< due "2026-02-15" >}} → "**Due:** Feb 15, 2026"
-- Formats a due date prominently
function due(args)
  local date_str = args[1] or "TBD"
  return pandoc.Strong({pandoc.Str("Due: " .. date_str)})
end

-- {{< hwmeta >}} - renders homework metadata banner from YAML frontmatter
-- Reads: due, grade-memo-due, estimated-time, submission from document metadata
-- Renders as a styled callout showing key dates and info
function hwmeta(args, kwargs, meta)
  local due_date = meta and meta["due"] and pandoc.utils.stringify(meta["due"]) or nil
  local memo_due = meta and meta["grade-memo-due"] and pandoc.utils.stringify(meta["grade-memo-due"]) or nil
  local est_time = meta and meta["estimated-time"] and pandoc.utils.stringify(meta["estimated-time"]) or nil
  local submission = meta and meta["submission"] and pandoc.utils.stringify(meta["submission"]) or nil

  if not due_date then
    return pandoc.RawBlock("html", "<!-- hwmeta: no due date in frontmatter -->")
  end

  local html = '<div class="callout callout-important" data-callout="important">\n'
  html = html .. '<div class="callout-header">\n<div class="callout-icon-container"><i class="callout-icon"></i></div>\n'
  html = html .. '<div class="callout-title-container flex-fill"><p class="callout-title">Assignment Info</p></div>\n</div>\n'
  html = html .. '<div class="callout-body-container callout-body">\n'
  html = html .. '<table class="hw-meta-table" style="width:100%; border-collapse:collapse;">\n'

  -- Due date (always shown)
  html = html .. string.format('<tr><td style="padding:0.25rem 0.5rem 0.25rem 0; font-weight:600; white-space:nowrap;">Due</td><td style="padding:0.25rem 0;">%s</td></tr>\n', due_date)

  -- Grade memo due (if present)
  if memo_due then
    html = html .. string.format('<tr><td style="padding:0.25rem 0.5rem 0.25rem 0; font-weight:600; white-space:nowrap;">Grade Memo</td><td style="padding:0.25rem 0;">%s</td></tr>\n', memo_due)
  end

  -- Estimated time (if present)
  if est_time then
    html = html .. string.format('<tr><td style="padding:0.25rem 0.5rem 0.25rem 0; font-weight:600; white-space:nowrap;">Est. Time</td><td style="padding:0.25rem 0;">%s</td></tr>\n', est_time)
  end

  -- Submission info (if present)
  if submission then
    html = html .. string.format('<tr><td style="padding:0.25rem 0.5rem 0.25rem 0; font-weight:600; white-space:nowrap;">Submit via</td><td style="padding:0.25rem 0;">%s</td></tr>\n', submission)
  end

  html = html .. '</table>\n</div>\n</div>'

  return pandoc.RawBlock("html", html)
end

-- {{< points 10 >}} → "(10 points)"
-- Shows point value for an assignment/question
function points(args)
  local pts = args[1] or "?"
  local label = tonumber(pts) == 1 and " point" or " points"
  return pandoc.Emph({pandoc.Str("(" .. pts .. label .. ")")})
end

-- {{< reading "Chapter 3" "pp. 45-62" >}} → "📖 Chapter 3, pp. 45-62"
-- Formats a reading assignment
function reading(args)
  local chapter = args[1] or ""
  local pages = args[2] or ""
  local text = chapter
  if pages ~= "" then
    text = text .. ", " .. pages
  end
  return pandoc.Span({pandoc.Str(text)}, {class = "reading-ref"})
end

-- {{< exam "Midterm 1" >}} → styled exam reference
function exam(args)
  local name = args[1] or "Exam"
  return pandoc.Strong({pandoc.Str(name)})
end

-- {{< week 3 >}} → "Week 3"
-- For schedule references
function week(args)
  local num = args[1] or "?"
  return pandoc.Str("Week " .. num)
end

-- {{< canvas "assignments" >}} → link to Canvas section
-- Generates Canvas deep link
function canvas(args)
  local section = args[1] or ""
  local url = "https://sdsu.instructure.com"
  local text = "Canvas"
  if section ~= "" then
    text = "Canvas " .. section
  end
  return pandoc.Link(text, url, "", {class = "canvas-link"})
end

-- {{< office-hours >}} → shows office hours from params
-- Pulls from metadata
function office_hours(args, kwargs, meta)
  local oh = "See syllabus"
  if meta and meta.params and meta.params["office-hours"] then
    oh = pandoc.utils.stringify(meta.params["office-hours"])
  end
  return pandoc.Str(oh)
end

-- {{< instructor >}} → shows instructor name from params
function instructor(args, kwargs, meta)
  local name = "Instructor"
  if meta and meta.params and meta.params["instructor"] then
    name = pandoc.utils.stringify(meta.params["instructor"])
  end
  return pandoc.Str(name)
end

-- {{< email >}} → mailto link to instructor
function email(args, kwargs, meta)
  local addr = "instructor@example.com"
  if meta and meta.params and meta.params["email"] then
    addr = pandoc.utils.stringify(meta.params["email"])
  end
  return pandoc.Link(addr, "mailto:" .. addr)
end

-- {{< semester >}} → shows semester from params
function semester(args, kwargs, meta)
  local sem = "Current Semester"
  if meta and meta.params and meta.params["semester"] then
    sem = pandoc.utils.stringify(meta.params["semester"])
  end
  return pandoc.Str(sem)
end

-- ==============================================================
-- Figure shortcode - renders figures from central registry
-- ==============================================================

local function normalize_yaml_value(value)
  if not value then return value end
  value = value:gsub("^%s+", ""):gsub("%s+$", "")

  -- Quoted strings: capture content up to closing quote, ignore trailing comments.
  local dq = value:match('^"([^"]*)"')
  if dq ~= nil then
    -- Minimal unescape for double-quoted YAML scalars so LaTeX backslashes
    -- survive registry parsing correctly.
    dq = dq:gsub("\\\\", "\0")
    dq = dq:gsub('\\"', '"')
    dq = dq:gsub("\\n", "\n")
    dq = dq:gsub("\\t", "\t")
    dq = dq:gsub("\\r", "\r")
    dq = dq:gsub("\0", "\\")
    return dq
  end

  local sq = value:match("^'([^']*)'")
  if sq ~= nil then return sq end

  -- Unquoted: strip inline comments.
  value = value:gsub("%s+#.*$", "")
  value = value:gsub("^%s+", ""):gsub("%s+$", "")
  return value
end

-- Helper function to parse figure data from YAML file
local function load_figure_registry()
  local registry = {}

  -- Try to find the figures.yml file from project root
  -- Quarto sets QUARTO_PROJECT_DIR when running
  local project_dir = os.getenv("QUARTO_PROJECT_DIR") or "."
  local registry_path = project_dir .. "/assets/figures.yml"

  local f = io.open(registry_path, "r")
  if not f then
    -- Fallback: try relative path (works from project root)
    f = io.open("assets/figures.yml", "r")
  end
  if not f then
    return registry
  end

  local content = f:read("*all")
  f:close()

  -- Parse YAML manually (simplified parser for our specific format)
  local current_fig = nil
  for line in content:gmatch("[^\n]+") do
    -- Skip comments and empty lines
    if not line:match("^%s*#") and not line:match("^%s*$") then
      -- Check for figure ID (two spaces + name + colon)
      local fig_id = line:match("^  ([%w%-_]+):%s*$")
      if fig_id then
        current_fig = fig_id
        registry[current_fig] = {}
      elseif current_fig then
        -- Parse properties (four spaces + key: value)
        local key, value = line:match("^    ([%w%-_]+):%s*(.+)$")
        if key and value then
          registry[current_fig][key] = normalize_yaml_value(value)
        end
      end
    end
  end

  return registry
end

-- Cache the registry to avoid re-reading on every shortcode call
local _figure_registry = nil
local function get_figure_registry()
  if not _figure_registry then
    _figure_registry = load_figure_registry()
  end
  return _figure_registry
end

-- ==============================================================
-- Media registry - videos/embeds (for slides)
-- ==============================================================

-- Helper function to parse media data from YAML file
local function load_media_registry()
  local registry = {}

  local project_dir = os.getenv("QUARTO_PROJECT_DIR") or "."
  local registry_path = project_dir .. "/assets/media.yml"

  local f = io.open(registry_path, "r")
  if not f then
    f = io.open("assets/media.yml", "r")
  end
  if not f then
    return registry
  end

  local content = f:read("*all")
  f:close()

  local in_media = false
  local current_id = nil

  for line in content:gmatch("[^\n]+") do
    if not line:match("^%s*#") and not line:match("^%s*$") then
      if line:match("^media:%s*$") then
        in_media = true
        current_id = nil
      elseif in_media then
        local media_id = line:match("^  ([%w%-_]+):%s*$")
        if media_id then
          current_id = media_id
          registry[current_id] = {}
        elseif current_id then
          local key, value = line:match("^    ([%w%-_]+):%s*(.+)$")
          if key and value then
            registry[current_id][key] = normalize_yaml_value(value)
          end
        end
      end
    end
  end

  return registry
end

local _media_registry = nil
local function get_media_registry()
  if not _media_registry then
    _media_registry = load_media_registry()
  end
  return _media_registry
end

local function escape_html(s)
  if not s then return "" end
  s = tostring(s)
  s = s:gsub("&", "&amp;")
  s = s:gsub("<", "&lt;")
  s = s:gsub(">", "&gt;")
  s = s:gsub('"', "&quot;")
  return s
end

local function extract_youtube_id(url)
  if not url or url == "" then return nil end

  local id = url:match("youtu%.be/([%w%-%_]+)")
  if id then return id end

  id = url:match("youtube%.com/embed/([%w%-%_]+)")
  if id then return id end

  id = url:match("[?&]v=([%w%-%_]+)")
  if id then return id end

  return nil
end

-- {{< fig id >}} or {{< fig id caption="Custom caption" >}}
-- {{< fig id layout="aside" >}} for side-by-side layout (image left, caption right)
-- {{< fig id layout="aside" width="40%" >}} with custom image width
-- Renders figure from central registry with optional caption override
function fig(args, kwargs)
  local fig_id = args[1]
  if not fig_id then
    return pandoc.Strong({pandoc.Str("[ERROR: fig shortcode requires figure ID]")})
  end

  local registry = get_figure_registry()
  local fig_data = registry[fig_id]

  if not fig_data then
    return pandoc.Strong({pandoc.Str("[ERROR: Figure '" .. fig_id .. "' not found in registry]")})
  end

  -- Get figure properties
  local path = fig_data.path or ""
  local caption = fig_data.caption or ""
  local alt = fig_data.alt or caption
  local credit = fig_data.credit

  -- Allow caption override via kwargs
  -- Only override if kwargs.caption has actual content (not empty Inlines list)
  if kwargs and kwargs.caption then
    local caption_override = pandoc.utils.stringify(kwargs.caption)
    if caption_override ~= "" then
      caption = caption_override
    end
  end

  -- Build full caption with credit if present
  local full_caption = caption
  if credit and credit ~= "" then
    full_caption = full_caption .. " (Credit: " .. credit .. ")"
  end

  -- Check for layout parameter
  local layout = nil
  if kwargs and kwargs.layout then
    layout = pandoc.utils.stringify(kwargs.layout)
  end

  -- Check for width parameter (used with aside layout)
  local width = nil
  if kwargs and kwargs.width then
    width = pandoc.utils.stringify(kwargs.width)
  end

  -- Parse caption as markdown to support formatting like **bold**
  local caption_doc = pandoc.read(full_caption, "markdown")
  local caption_inlines = {}
  if caption_doc and caption_doc.blocks and #caption_doc.blocks > 0 then
    local first_block = caption_doc.blocks[1]
    if first_block.content then
      caption_inlines = first_block.content
    elseif first_block.t == "Plain" or first_block.t == "Para" then
      caption_inlines = first_block.content or {}
    end
  end

  -- Side-by-side layout: image left, caption right
  if layout == "aside" then
    local width_style = width and string.format(' style="max-width: %s;"', width) or ""

    -- Convert caption markdown to HTML for proper rendering
    local caption_html = full_caption
    local caption_doc = pandoc.read(full_caption, "markdown")
    if caption_doc and caption_doc.blocks and #caption_doc.blocks > 0 then
      -- Write just the inlines as HTML (strip wrapping <p> tags)
      caption_html = pandoc.write(caption_doc, "html")
      -- Remove outer <p> tags if present
      caption_html = caption_html:gsub("^<p>(.+)</p>%s*$", "%1")
    end

    local html = string.format([[
<div id="fig-%s" class="figure course-figure figure-aside">
  <div class="figure-content"%s>
    <img src="%s" alt="%s">
  </div>
  <div class="figure-caption">
    <p><em>%s</em></p>
  </div>
</div>
]], fig_id, width_style, path, alt, caption_html)
    return pandoc.RawBlock("html", html)
  end

  -- Default vertical layout: image on top, caption below
  local img = pandoc.Image({pandoc.Str(alt)}, path)
  local img_para = pandoc.Para({img})

  -- Wrap in italics for figure caption styling
  local caption_para = pandoc.Para({pandoc.Emph(caption_inlines)})

  local figure_div = pandoc.Div(
    {img_para, caption_para},
    pandoc.Attr("fig-" .. fig_id, {"figure", "course-figure"})
  )

  return figure_div
end

-- {{< img id >}} - renders image from registry WITHOUT caption (for slides)
-- Optional kwargs: width, height, class, trim (like LaTeX)
-- trim="0 50% 0 0" → clip-path: inset(0 50% 0 0)
function img(args, kwargs)
  local fig_id = args[1]
  if not fig_id then
    return pandoc.Strong({pandoc.Str("[ERROR: img shortcode requires figure ID]")})
  end

  local registry = get_figure_registry()
  local fig_data = registry[fig_id]

  if not fig_data then
    return pandoc.Strong({pandoc.Str("[ERROR: Image '" .. fig_id .. "' not found in registry]")})
  end

  -- Get figure properties
  local path = fig_data.path or ""
  local alt = fig_data.alt or fig_data.caption or ""
  local credit = fig_data.credit or ""

  -- Build attributes from kwargs
  local classes = {}
  local attrs = {}

  if kwargs["class"] then
    local class_str = pandoc.utils.stringify(kwargs["class"])
    for class in class_str:gmatch("%S+") do
      table.insert(classes, class)
    end
  end

  if kwargs["width"] then
    attrs["width"] = pandoc.utils.stringify(kwargs["width"])
  end

  if kwargs["height"] then
    attrs["height"] = pandoc.utils.stringify(kwargs["height"])
  end

  -- trim="top right bottom left" → scale + clip (like LaTeX trim)
  local trim_val = nil
  if kwargs["trim"] then
    local trim_raw = kwargs["trim"]
    if type(trim_raw) == "string" then
      trim_val = trim_raw
    elseif type(trim_raw) == "table" and trim_raw.text then
      trim_val = trim_raw.text
    else
      trim_val = pandoc.utils.stringify(trim_raw)
    end
  end

  -- If trim specified, scale image so visible portion fills container
  if trim_val and trim_val ~= "" then
    local t, r, b, l = trim_val:match("(%S+)%s+(%S+)%s+(%S+)%s+(%S+)")
    if t and r and b and l then
      -- Convert percentages to numbers
      local function to_num(s)
        local n = tonumber(s:match("(%d+)"))
        return n and n/100 or 0
      end
      local tn, rn, bn, ln = to_num(t), to_num(r), to_num(b), to_num(l)

      -- Scale factors to make visible portion fill container
      local scale_x = 1 / (1 - ln - rn)
      local scale_y = 1 / (1 - tn - bn)

      local img_style = string.format(
        "transform:scale(%.3f, %.3f); transform-origin:%s %s; clip-path:inset(%s %s %s %s);",
        scale_x, scale_y,
        ln > 0 and "right" or "left",
        tn > 0 and "bottom" or "top",
        t, r, b, l
      )

      local class_attr = ""
      if #classes > 0 then
        class_attr = string.format(' class="%s"', escape_html(table.concat(classes, " ")))
      end

      local width_attr = ""
      if attrs["width"] then
        width_attr = string.format(' width="%s"', escape_html(attrs["width"]))
      end

      local height_attr = ""
      if attrs["height"] then
        height_attr = string.format(' height="%s"', escape_html(attrs["height"]))
      end

      if credit and credit ~= "" then
        local html = string.format([[
<div class="media-block media-image">
  <img src="%s" alt="%s"%s%s%s style="%s">
  <div class="media-credit">Credit: %s</div>
</div>
]], escape_html(path), escape_html(alt), class_attr, width_attr, height_attr, escape_html(img_style), escape_html(credit))
        return pandoc.RawBlock("html", html)
      end

      local img_with_style = pandoc.Image({pandoc.Str(alt)}, path, "", pandoc.Attr("", classes, {style = img_style}))
      return img_with_style
    end
  end

  -- No trim, return plain image
  if credit and credit ~= "" then
    local class_attr = ""
    if #classes > 0 then
      class_attr = string.format(' class="%s"', escape_html(table.concat(classes, " ")))
    end

    local width_attr = ""
    if attrs["width"] then
      width_attr = string.format(' width="%s"', escape_html(attrs["width"]))
    end

    local height_attr = ""
    if attrs["height"] then
      height_attr = string.format(' height="%s"', escape_html(attrs["height"]))
    end

    local html = string.format([[
<div class="media-block media-image">
  <img src="%s" alt="%s"%s%s%s>
  <div class="media-credit">Credit: %s</div>
</div>
]], escape_html(path), escape_html(alt), class_attr, width_attr, height_attr, escape_html(credit))
    return pandoc.RawBlock("html", html)
  end

  local img_elem = pandoc.Image({pandoc.Str(alt)}, path, "", pandoc.Attr("", classes, attrs))
  return img_elem
end

-- {{< media id >}} - renders media from registry WITH credit (for slides)
-- Optional kwargs: width, height, class
function media(args, kwargs)
  local media_id = args[1]
  if not media_id then
    return pandoc.Strong({pandoc.Str("[ERROR: media shortcode requires media ID]")})
  end

  local registry = get_media_registry()
  local media_data = registry[media_id]

  if not media_data then
    return pandoc.Strong({pandoc.Str("[ERROR: Media '" .. media_id .. "' not found in registry]")})
  end

  local url = media_data.url or ""
  local credit = media_data.credit

  if credit == nil then
    return pandoc.Strong({pandoc.Str("[ERROR: Media '" .. media_id .. "' missing required field: credit]")})
  end

  local classes = {"media-block", "media-video"}
  if kwargs and kwargs["class"] then
    local class_str = pandoc.utils.stringify(kwargs["class"])
    for class in class_str:gmatch("%S+") do
      table.insert(classes, class)
    end
  end

  local width = "100%"
  local height = nil
  local height_set = false
  if kwargs and kwargs["width"] then
    width = pandoc.utils.stringify(kwargs["width"])
  end
  if kwargs and kwargs["height"] then
    height = pandoc.utils.stringify(kwargs["height"])
    height_set = true
  end

  local class_attr = string.format(' class="%s"', escape_html(table.concat(classes, " ")))

  local credit_html = ""
  if credit ~= "" then
    credit_html = string.format('\n  <div class="media-credit">Credit: %s</div>', escape_html(credit))
  end

  local yt_id = extract_youtube_id(url)
  if yt_id then
    local src = "https://www.youtube-nocookie.com/embed/" .. yt_id
    local style_attr = string.format(' style="width:%s;%s"', escape_html(width), height_set and (" height:" .. escape_html(height) .. ";") or " aspect-ratio:16/9;")
    local html = string.format([[
<div%s%s>
  <iframe class="media-embed" src="%s" title="YouTube video" frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen></iframe>%s
</div>
]], class_attr, style_attr, escape_html(src), credit_html)
    return pandoc.RawBlock("html", html)
  end

  -- Fallback: render as iframe for unknown providers
  local style_attr = string.format(' style="width:%s;%s"', escape_html(width), height_set and (" height:" .. escape_html(height) .. ";") or " aspect-ratio:16/9;")
  local html = string.format([[
<div%s%s>
  <iframe class="media-embed" src="%s" title="Embedded media" frameborder="0" allowfullscreen></iframe>%s
</div>
]], class_attr, style_attr, escape_html(url), credit_html)
  return pandoc.RawBlock("html", html)
end

-- ==============================================================
-- Equation System Shortcodes
-- ==============================================================

-- Process YAML escape sequences in double-quoted strings
local function process_yaml_escapes(s)
  if not s then return s end
  -- Process common YAML escape sequences
  s = s:gsub("\\\\", "\000BACKSLASH\000")  -- Placeholder for literal backslash
  s = s:gsub("\\n", "\n")
  s = s:gsub("\\t", "\t")
  s = s:gsub("\\\"", '"')
  s = s:gsub("\000BACKSLASH\000", "\\")    -- Restore single backslash
  return s
end

-- Load eqcards.yml (meaning scaffolds)
local function load_eqcards()
  local cards = {}
  local project_dir = os.getenv("QUARTO_PROJECT_DIR") or "."
  local path = project_dir .. "/data/eqcards.yml"

  local f = io.open(path, "r")
  if not f then
    f = io.open("data/eqcards.yml", "r")
  end
  if not f then return cards end

  local content = f:read("*all")
  f:close()

  -- Parse YAML (adapted for eqcards format with arrays)
  local current_id = nil
  local in_assumptions = false

  for line in content:gmatch("[^\n]+") do
    if not line:match("^%s*#") and not line:match("^%s*$") then
      -- Top-level card ID (no indent, ends with colon)
      local card_id = line:match("^([%w_]+):%s*$")
      if card_id then
        current_id = card_id
        cards[current_id] = { assumptions = {} }
        in_assumptions = false
      elseif current_id then
        -- Nested key-value (2-space indent)
        local key, val = line:match("^  ([%w_]+):%s*\"(.-)\"$")
        if not key then
          key, val = line:match("^  ([%w_]+):%s*(.+)$")
        end
        if key and val and val ~= "" then
          cards[current_id][key] = process_yaml_escapes(val)
          in_assumptions = false
        elseif line:match("^  assumptions:%s*$") then
          in_assumptions = true
        elseif in_assumptions then
          -- Array item (4-space indent with -)
          local item = line:match("^    %- \"(.-)\"$")
          if not item then
            item = line:match("^    %- (.+)$")
          end
          if item then
            table.insert(cards[current_id].assumptions, process_yaml_escapes(item))
          end
        end
      end
    end
  end

  return cards
end

-- Load equations.yml (registry)
local function load_equations()
  local eqs = {}
  local project_dir = os.getenv("QUARTO_PROJECT_DIR") or "."
  local path = project_dir .. "/data/equations.yml"

  local f = io.open(path, "r")
  if not f then
    f = io.open("data/equations.yml", "r")
  end
  if not f then return eqs end

  local content = f:read("*all")
  f:close()

  local current_id = nil

  for line in content:gmatch("[^\n]+") do
    if not line:match("^%s*#") and not line:match("^%s*$") then
      local eq_id = line:match("^([%w_%-]+):%s*$")
      if eq_id then
        current_id = eq_id
        eqs[current_id] = {}
      elseif current_id then
        local key, val = line:match("^  ([%w_]+):%s*\"(.-)\"$")
        if not key then
          key, val = line:match("^  ([%w_]+):%s*(.+)$")
        end
        if key and val then
          eqs[current_id][key] = process_yaml_escapes(val)
        end
      end
    end
  end

  return eqs
end

-- Cache for equation data
local _eqcards_cache = nil
local _equations_cache = nil

local function get_eqcards()
  if not _eqcards_cache then
    _eqcards_cache = load_eqcards()
  end
  return _eqcards_cache
end

local function get_equations()
  if not _equations_cache then
    _equations_cache = load_equations()
  end
  return _equations_cache
end

-- Helper: convert $...$ math to HTML spans that MathJax will process
-- MathJax doesn't auto-process $...$ in raw HTML blocks, so we wrap in spans
local function convert_math_for_html(text)
  if not text then return "" end
  -- Convert $...$ to <span class="math inline">\(...\)</span>
  -- This is the format Pandoc outputs and MathJax is configured to process
  text = text:gsub("%$([^$]+)%$", '<span class="math inline">\\(%1\\)</span>')
  return text
end

-- Helper: build meaning card HTML
local function build_meaning_html(card, title, anchor)
  -- Convert LaTeX delimiters in all fields
  local predicts = convert_math_for_html(card.predicts or "")
  local depends = convert_math_for_html(card.depends or "")
  local says = convert_math_for_html(card.says or "")

  local html = string.format([[
<div class="callout callout-tip eq-gloss" data-callout="tip">
  <div class="callout-header">
    <div class="callout-title-container flex-fill">
      <p class="callout-title">%s</p>
    </div>
  </div>
  <div class="callout-body-container callout-body">
    <p><strong>What it predicts</strong><br/>%s</p>
    <p><strong>What it depends on</strong><br/>%s</p>
    <p><strong>What it's saying</strong><br/>%s</p>
]], title or "Equation meaning", predicts, depends, says)

  if card.assumptions and #card.assumptions > 0 then
    html = html .. "    <p><strong>Assumptions</strong></p>\n    <ul>\n"
    for _, a in ipairs(card.assumptions) do
      html = html .. "      <li>" .. convert_math_for_html(a) .. "</li>\n"
    end
    html = html .. "    </ul>\n"
  end

  if anchor then
    html = html .. string.format('    <p style="margin-top:0.5rem;"><em>See:</em> <a href="#%s">the equation</a></p>\n', anchor)
  end

  html = html .. "  </div>\n</div>"
  return html
end

-- {{< eqcard kepler_period >}} - show meaning scaffold only
function eqcard(args, kwargs)
  -- Use args[1] directly (Quarto args are special Pandoc objects)
  local cards = get_eqcards()
  local card = cards[args[1]]

  if not card then
    return pandoc.RawBlock("html", string.format('<div class="callout callout-warning"><p><strong>Missing eqcard:</strong> <code>%s</code></p></div>', tostring(args[1] or "nil")))
  end

  return pandoc.RawBlock("html", build_meaning_html(card, "Equation meaning", nil))
end

-- {{< eqrefcard kepler >}} - show meaning + reference link
function eqrefcard(args, kwargs)
  -- Try direct access without intermediate variable
  local equations = get_equations()
  local eq = equations[args[1]]  -- Direct access like eqcard does

  if not eq and kwargs and kwargs["eq"] then
    eq = equations[kwargs["eq"]]
  end

  if not eq then
    local keys = {}
    for k in pairs(equations) do table.insert(keys, k) end
    return pandoc.RawBlock("html", string.format('<div class="callout callout-warning"><p><strong>Equation not found:</strong> tostring=%s type=%s. Available: %s</p></div>', tostring(args[1]), type(args[1]), table.concat(keys, ", ")))
  end

  local cards = get_eqcards()
  local card = cards[eq.card]

  if not card then
    return pandoc.RawBlock("html", string.format('<div class="callout callout-warning"><p><strong>Missing eqcard:</strong> <code>%s</code></p></div>', eq.card or "nil"))
  end

  return pandoc.RawBlock("html", build_meaning_html(card, eq.title, eq.anchor))
end

-- {{< eqshow kepler >}} - title + meaning (use with include for equation)
function eqshow(args, kwargs)
  -- Use args[1] directly in table lookup (Quarto args are special Pandoc objects)
  local equations = get_equations()
  local eq = equations[args[1]]

  if not eq and kwargs and kwargs["eq"] then
    eq = equations[kwargs["eq"]]
  end

  if not eq then
    return pandoc.RawBlock("html", string.format('<div class="callout callout-warning"><p><strong>Missing equation:</strong> <code>%s</code></p></div>', tostring(args[1] or "nil")))
  end

  local cards = get_eqcards()
  local card = cards[eq.card]

  local blocks = {}

  -- Title
  table.insert(blocks, pandoc.RawBlock("html", string.format('<p class="eq-title" style="margin:0.4rem 0 0.35rem 0;"><strong>%s</strong></p>', eq.title or "")))

  -- Note about include (Lua cannot dynamically include files)
  table.insert(blocks, pandoc.RawBlock("html", string.format('<!-- Use: {{< include %s >}} above this shortcode -->', eq.include or "")))

  -- Meaning card
  if card then
    table.insert(blocks, pandoc.RawBlock("html", build_meaning_html(card, "Equation meaning", eq.anchor)))
  else
    table.insert(blocks, pandoc.RawBlock("html", string.format('<div class="callout callout-warning"><p><strong>Missing eqcard:</strong> <code>%s</code></p></div>', eq.card or "nil")))
  end

  return blocks
end

-- {{< eqindex >}} - auto-generated catalog of all equations
function eqindex(args, kwargs)
  local equations = get_equations()
  local cards = get_eqcards()

  if not equations or not next(equations) then
    return pandoc.RawBlock("html", '<div class="callout callout-warning"><p>No equations found. Expected <code>data/equations.yml</code>.</p></div>')
  end

  -- Sort keys alphabetically
  local keys = {}
  for k in pairs(equations) do
    table.insert(keys, k)
  end
  table.sort(keys)

  local html = '<div class="eq-index">\n'

  for _, k in ipairs(keys) do
    local eq = equations[k]
    local card = cards[eq.card]

    html = html .. '<div class="eq-index-item">\n'
    html = html .. '  <h3 class="eq-index-title" style="margin:0 0 0.35rem 0;">'
    if eq.anchor then
      html = html .. string.format('<a href="#%s">%s</a>', eq.anchor, eq.title or k)
    else
      html = html .. (eq.title or k)
    end
    html = html .. '</h3>\n'

    if card then
      html = html .. '  <div class="eq-index-gloss">\n'
      html = html .. string.format('    <p style="margin:0.25rem 0;"><strong>Predicts:</strong> %s</p>\n', card.predicts or "")
      html = html .. string.format('    <p style="margin:0.25rem 0;"><strong>Depends:</strong> %s</p>\n', card.depends or "")
      html = html .. string.format('    <p style="margin:0.25rem 0;"><strong>Says:</strong> %s</p>\n', card.says or "")
      if card.assumptions and #card.assumptions > 0 then
        html = html .. '    <details style="margin-top:0.35rem;">\n      <summary><strong>Assumptions</strong></summary>\n      <ul style="margin-top:0.35rem;">\n'
        for _, a in ipairs(card.assumptions) do
          html = html .. '        <li>' .. a .. '</li>\n'
        end
        html = html .. '      </ul>\n    </details>\n'
      end
      html = html .. '  </div>\n'
    else
      html = html .. string.format('  <div class="callout callout-warning"><p>Missing eqcard: <code>%s</code></p></div>\n', eq.card or "nil")
    end

    html = html .. string.format('  <p class="eq-index-meta" style="opacity:0.7; margin:0.4rem 0 0; font-size:0.85em;">id: <code>%s</code></p>\n', k)
    html = html .. '</div>\n'
  end

  html = html .. '</div>'

  return pandoc.RawBlock("html", html)
end

-- ==============================================================
-- Glossary System Shortcodes
-- ==============================================================

-- Load glossary.yml
local function load_glossary()
  local terms = {}
  local project_dir = os.getenv("QUARTO_PROJECT_DIR") or "."
  local path = project_dir .. "/data/glossary.yml"

  local f = io.open(path, "r")
  if not f then
    f = io.open("data/glossary.yml", "r")
  end
  if not f then return terms end

  local content = f:read("*all")
  f:close()

  -- Parse YAML (adapted for glossary format)
  local current_id = nil
  for line in content:gmatch("[^\n]+") do
    if not line:match("^%s*#") and not line:match("^%s*$") then
      -- Top-level term ID (no indent, ends with colon)
      local term_id = line:match("^([%w_]+):%s*$")
      if term_id then
        current_id = term_id
        terms[current_id] = {}
      elseif current_id then
        -- Nested key-value (2-space indent)
        local key, val = line:match("^  ([%w_]+):%s*\"(.-)\"$")
        if not key then
          key, val = line:match("^  ([%w_]+):%s*(.+)$")
        end
        if key and val and val ~= "" then
          -- Remove surrounding quotes if present
          val = val:gsub('^"(.+)"$', "%1")
          terms[current_id][key] = process_yaml_escapes(val)
        end
      end
    end
  end

  return terms
end

-- Cache
local _glossary_cache = nil
local function get_glossary()
  if not _glossary_cache then
    _glossary_cache = load_glossary()
  end
  return _glossary_cache
end

-- {{< term id >}} - inline term with margin definition
-- Returns the term name and creates a margin note with definition
function term(args, kwargs)
  local term_id = args[1]
  if not term_id then
    return pandoc.Strong({pandoc.Str("[ERROR: term requires ID]")})
  end

  local glossary = get_glossary()
  local entry = glossary[term_id]

  if not entry then
    return pandoc.Strong({pandoc.Str("[Unknown term: " .. term_id .. "]")})
  end

  local term_name = entry.term or term_id
  local definition = entry.definition or ""

  -- Parse definition as markdown (handles LaTeX)
  local def_doc = pandoc.read(definition, "markdown")
  local def_inlines = {}
  if def_doc and def_doc.blocks and #def_doc.blocks > 0 then
    local first = def_doc.blocks[1]
    if first.content then
      def_inlines = first.content
    end
  end

  -- Create margin note with definition
  local margin_content = {
    pandoc.Strong({pandoc.Str(term_name .. ":")}),
    pandoc.Space(),
  }
  for _, inline in ipairs(def_inlines) do
    table.insert(margin_content, inline)
  end

  local margin_note = pandoc.Span(
    margin_content,
    pandoc.Attr("", {"column-margin", "term-definition"})
  )

  -- Return term in bold + margin note (Quarto processes .column-margin class)
  return {pandoc.Strong({pandoc.Str(term_name)}), margin_note}
end

-- {{< defn id >}} - just the definition (for manual placement)
function defn(args, kwargs)
  local term_id = args[1]
  if not term_id then
    return pandoc.Str("")
  end

  local glossary = get_glossary()
  local entry = glossary[term_id]

  if not entry then
    return pandoc.Str("")
  end

  local definition = entry.definition or ""

  -- Parse as markdown
  local def_doc = pandoc.read(definition, "markdown")
  if def_doc and def_doc.blocks and #def_doc.blocks > 0 then
    local first = def_doc.blocks[1]
    if first.content then
      return first.content
    end
  end

  return pandoc.Str(definition)
end

-- {{< glossary >}} or {{< glossary module=1 >}} or {{< glossary first_use="Lecture 3" >}} - full glossary section
function glossary(args, kwargs)
  local glossary_data = get_glossary()
  local filter_module = nil
  local filter_first_use = nil

  if kwargs and kwargs.module then
    filter_module = tonumber(pandoc.utils.stringify(kwargs.module))
  end
  if kwargs and kwargs.first_use then
    filter_first_use = pandoc.utils.stringify(kwargs.first_use)
  end

  if not glossary_data or not next(glossary_data) then
    return pandoc.RawBlock("html", '<div class="callout callout-warning"><p>No glossary found.</p></div>')
  end

  -- Sort keys alphabetically by term name
  local sorted = {}
  for id, entry in pairs(glossary_data) do
    -- Filter by module if specified
    local module_match = not filter_module or (entry.module and tonumber(entry.module) == filter_module)
    -- Filter by first_use if specified
    local first_use_match = not filter_first_use or (entry.first_use and entry.first_use == filter_first_use)
    if module_match and first_use_match then
      table.insert(sorted, {id = id, entry = entry, sort_key = (entry.term or id):lower()})
    end
  end
  table.sort(sorted, function(a, b) return a.sort_key < b.sort_key end)

  local html = '<div class="glossary">\n<dl>\n'

  for _, item in ipairs(sorted) do
    local entry = item.entry
    local term_name = entry.term or item.id
    local definition = convert_math_for_html(entry.definition or "")
    local context = convert_math_for_html(entry.context or "")

    html = html .. string.format('  <dt id="glossary-%s"><strong>%s</strong></dt>\n', item.id, term_name)
    html = html .. string.format('  <dd>%s', definition)
    if context ~= "" then
      html = html .. string.format(' <em>%s</em>', context)
    end
    html = html .. '</dd>\n'
  end

  html = html .. '</dl>\n</div>'

  return pandoc.RawBlock("html", html)
end
