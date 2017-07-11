var import_mathjax = '<script type="text/x-mathjax-config"> \
                      MathJax.Hub.Config({ \
                          skipStartupTypeset: true, \
                          tex2jax: { \
                                inlineMath: [["$", "$"]], \
                                displayMath: [["$$", "$$"]], \
                          }, \
                          processEscapes: true,\
                      }) \
                      </script>\
                      <script async type="text/javascript" src="/static/parts/MathJax/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>';

document.write(import_mathjax);
function latex_support(plainText) {
    plainText = SimpleMDE.prototype.markdown(plainText);
    $("#create-update-form").append("<div id='latex-render-area' style='display: none'></div>");
    $("#latex-render-area").append(plainText);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, 'latex-render-area']);
    plainText = $("#latex-render-area").html();
    $("#latex-render-area").remove();
    return plainText;
}
