pelican-toc
===================================

This plugin generates a table of contents for pelican articles and pages, available for themes via `article.toc`.

#Differences between pelican-toc and pelican-extract-toc
`extract-toc` uses a markdown extension to generate a toc and then extract it via beautifulsoup. This extension generates the toc itself, removing the need to write `[ToC]` in your articles. Also there is a 'health' check on id's which should be generated via markdown.extensions.headerid per default, but somehow don't always end up in the output. 

#Usage
##requirements
Beautifulsoup4 - install via `pip install beautifulsoup4`
##theme
```
{% if article.toc %}
<div class="col-lg-3 hidden-xs hidden-sm">
    {{article.toc}}
</div>
{% endif %}
```
##article
```
Title: Peeking at erlang/chicagoboss
###Intro
###Chicagoboss Magic
###Result
```
##output
```
<div class="col-lg-3 hidden-xs hidden-sm">
    <div id="toc">
      <ul>
        <li>
          <a href="#" title="Peeking at&nbsp;erlang/chicagoboss">Peeking at&nbsp;erlang/chicagoboss</a>
          <ul>
            <li>
              <a href="#intro" title="Intro">Intro</a>
            </li>
            <li>
              <a href="#chicagoboss-magic" title="Chicagoboss&nbsp;Magic">Chicagoboss&nbsp;Magic</a>
            </li>
            <li>
              <a href="#result" title="Result">Result</a>
            </li>
          </ul>
        </li>
      </ul>
    </div>
</div>
```

#Todo
*   options for toc generation either via config/metadata
