from html.parser import HTMLParser


class TootParser(HTMLParser):
    content = ''
    span_levels = 0

    def handle_starttag(self, tag, _):
        if tag == 'span':
            self.span_levels += 1
        elif tag == 'br':
            self.content += '\n'

    def handle_data(self, data):
        if self.span_levels == 0:
            self.content += data

    def handle_endtag(self, tag):
        if tag == 'span':
            self.span_levels -= 1
        # when a two consecutive line breaks appear in a post,
        # mastodon server converts block above and below to
        # <p>first<br />block</p><p>second<br />block</p>
        elif tag == 'p':
            self.content += '\n'


if __name__ == '__main__':
    toot_parser = TootParser()
    toot_parser.feed(
        '<p><span class=\"h-card\"><a href=\"https://linuxrocks.online/@hund\" class=\"u-url mention\">@<span>hund</span></a></span> <br />Libre: <br />+ unambiguous<br />+ French pronunciation makes it classy<br />- relatively hard to pronounce<br />- difficult to explain to outsiders<br />- has an indescribable association with LibreOffice</p><p>Free:<br />+ Has the &quot;free as in freedom, not in beer&quot; slogan<br />+ FSF literally stands for that<br />+ the acronym FOSS enables me to clearly distinguish free and $0<br />- causes confusion where &quot;free&quot; software costs money*, eg. ardour<br />- sometimes mislabeled as &quot;FREE&quot;</p><p>I voted for Free.</p><p>* Pre-built binaries</p>'
    )

    print(toot_parser.content)
