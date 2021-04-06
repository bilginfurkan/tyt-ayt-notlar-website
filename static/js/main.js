if (typeof markdownData !== 'undefined') {
    let md = window.markdownit();
    let render = md.render(markdownData);
    render = render.replace(/!\[\[(.+)\]\]/g, "<img src='/medya/$1'>")

    $('#content').html(render);
}