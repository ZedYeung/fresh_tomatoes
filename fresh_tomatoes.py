import webbrowser
import item_class
import os
import re
import random


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #video .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        #book .modal-dialog {
            margin-top: 10px;
            width: 800px;
            height: 800px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #item-show {
            width: 100%;
            height: 100%;
        }
        .item-tile {
            margin-bottom: 50px;
            padding-top: 20px;
        }
        .item-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        /* navigation bar is mainly from https://www.w3schools.com/css/css_navbar.asp */
        ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #333;
        }

        li {
            float: left;
        }

        li a {
            display: block;
            color: white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
        }

        /* Change the link color to #111 (black) on hover */
        li a:hover {
            background-color: #111;
        }
        /* Change the current link color to #CC181E (red) */
        .active {
            background-color: #CC181E;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $(".scale-media").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.item-tile', function (event) {
            var sourceUrl = $(this).attr('data-source-url');
            var type = $(this).attr('data-target');
            if (type === '#video') {
                $("#video-show-container").empty().append($("<iframe></iframe>", {
                  'id': 'item-show',
                  'type': 'text-html',
                  'src': sourceUrl,
                  'frameborder': 0
                }));
            } else {
                $("#book-show-container").empty().append($("<iframe></iframe>", {
                  'id': 'item-show',
                  'type': 'text-html',
                  'src': sourceUrl,
                  'frameborder': 0
                }));
            }
        });
        // Animate in the items when the page loads
        $(document).ready(function () {
          $('.item-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Video Modal -->
    <div class="modal" id="video">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="video-show-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Book Modal -->
    <div class="modal" id="book">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="book-show-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <ul>
              <li class="active"><a href="fresh_tomatoes.html">Fresh Tomatoes</a></li>
              {navbar}
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {tiles}
    </div>
  </body>
</html>
'''

# A single navbar entry html template
navbar_content = '''
 <li><a href="{category_url}">{nav_title}</a></li>
 '''

# A single item entry html template
tile_content = '''
<div class="col-md-6 col-lg-4 item-tile text-center" data-source-url="{source_url}" data-toggle="modal" data-target="#{modal_class}">
    <img src="{poster_image_url}" width="220" height="320">
    <h2>{title}</h2>
</div>
'''


def create_tiles_content(items):
    # The HTML content for this section of the page
    content = ''

    for item in items:
        if not isinstance(item, item_class.Book):
            # Extract the youtube ID from the url
            youtube_id_match = re.search(
                r'(?<=v=)[^&#]+', item.url)
            youtube_id_match = youtube_id_match or re.search(
                r'(?<=be/)[^&#]+', item.url)
            trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                                  else None)
            source_url = 'http://www.youtube.com/embed/' + trailer_youtube_id + '?autoplay=1&html5=1'

        # Append the tile for the item with its content filled in
        content += tile_content.format(
            title=item.title,
            poster_image_url=item.poster,
            source_url=item.url if isinstance(item, item_class.Book) else source_url,
            modal_class='book' if isinstance(item, item_class.Book) else 'video'
        )

    return content


def open_page(items_list):
    home_page_items = []
    navbar = ''

    # get navigation bar
    for items in items_list:
        # identify the items class
        cat = re.search(r'(?<=item_class\.).*(?=\'>)', str(type(items[0]))).group(0)
        navbar += navbar_content.format(
            category_url=cat + '.html',
            nav_title=cat
        )

    # generate website according to category
    for items in items_list:
        cat = re.search(r'(?<=item_class\.).*(?=\'>)', str(type(items[0]))).group(0)
        random.shuffle(items)
        home_page_items.extend(items[:3])
        # Replace the item tiles placeholder generated content
        rendered_content = main_page_content.format(navbar=navbar,
            tiles=create_tiles_content(items))
        with open(cat + '.html', 'w') as f:
            f.write(main_page_head + rendered_content)

    # generate the home page
    output_file = open('fresh_tomatoes.html', 'w')
    # Replace the item tiles placeholder generated content
    rendered_content = main_page_content.format(navbar=navbar,
        tiles=create_tiles_content(home_page_items))
    print(home_page_items)

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
