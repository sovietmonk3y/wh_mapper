var paper;

$(document).ready(function() {
    $('select').on('change', function() {
        if(this.value) window.location = '/' + this.value;
    });

    $('#create-page').on('click', function(e) {
        e.preventDefault();

        if($('body').children('.new-page-form').length) return;

        var $formDiv = $(this).after($('#stash .new-page-form')).next();
        $formDiv.find('#page-name').focus();
        $formDiv.find('#system-name').autocomplete({
            source: function(request, response) {
                var $input = this.element;
                $.ajax({
                    type: 'GET',
                    url: '/api/system/autocomplete/' + request.term + '/',
                    success: function(data) {
                        var dataArray = JSON.parse(data);
                        if(dataArray.length == 1) {
                            $input.val(dataArray[0]);
                            response();
                        }
                        else response(dataArray);
                    }
                });
            }
        });
    });

    $('body').on('submit', '.new-page-form', function(e) {
        e.preventDefault();

        var $formDiv = $(this);

        var pageName = $formDiv.find('#page-name').val().trim();
        if(pageName == '') {
            alert('A valid page name must be entered.');
            return;
        }

        var systemName = $formDiv.find('#system-name').val().trim();
        if(systemName == '') {
            alert('A valid system name must be entered.');
            return;
        }

        $.ajax({
            type: 'POST',
            url: '/api/system_node/',
            data: {
                'system': systemName,
                'page_name': pageName
            },
            success: function() {
                window.location = '/' + pageName;
            },
            error: function(xhr) {
                alert(xhr.responseText);
            }
        });
    });

    if(typeof(systemTree) != "undefined" && systemTree != null && systemTreeLength) {

        document.onclick = function(e) {
            var tag_name = e.target.tagName.toLowerCase();
            if(tag_name != 'ellipse' && tag_name != 'text' && tag_name != 'tspan' &&
               tag_name != 'a' && !$(e.target).closest('form').length) {
                ClearSelection();
            }
        };

        document.onkeydown = function(e) {
            if(e.which == 27) ClearSelection();
        };

        $('#systemsHolder').on('click', '#add-connection', function(e) {
            e.preventDefault();

            var $stashConnectionForm = $('#stash .system-connection-form');
            var $container = $(this).parent();
            $container.html($stashConnectionForm.html());
            $container.attr('class', $stashConnectionForm.attr('class'));
            $container.find('#system-name').focus().autocomplete({
                select: function(event, ui) {
                    $(this).closest('form').find('input:submit').removeAttr('disabled');
                },
                source: function(request, response) {
                    var $input = this.element;
                    var $submit = $input.closest('form').find('input:submit');
                    $.ajax({
                        type: 'GET',
                        url: '/api/system/autocomplete/' + request.term + '/',
                        success: function(data) {
                            var dataArray = JSON.parse(data);
                            if(dataArray.length == 1) {
                                $input.val(dataArray[0]);
                                $submit.removeAttr('disabled');
                                response();
                            }
                            else {
                                $submit.attr('disabled', true);
                                response(dataArray);
                            }
                        }
                    });
                }
            });
        });

        $('#systemsHolder').on('click', '#delete-system', function(e) {
            e.preventDefault();

            $.ajax({
                type: 'DELETE',
                url: '/api/system_node/' +
                    paper.getById($(this).parent().attr('data-ellipse-id')).system.id + '/',
                success: function() {
                    window.location = '';
                },
                error: function(xhr) {
                    alert(xhr.responseText);
                }
            });
        });

        $('#systemsHolder').on('submit', '.system-connection-form', function(e) {
            e.preventDefault();

            var $formDiv = $(this);

            var systemName = $formDiv.find('#system-name').val().trim();
            if($formDiv.find('input:submit:disabled').length || systemName == '') {
                alert('A valid system name must be entered.');
                return;
            }

            $.ajax({
                type: 'POST',
                url: '/api/system_node/',
                data: {
                    'system': systemName,
                    'page_name': $('select').val(),
                    'parent_node': paper.getById($formDiv.attr('data-ellipse-id')).system.id
                },
                success: function() {
                    window.location = '';
                },
                error: function(xhr) {
                    alert(xhr.responseText);
                }
            });
        });

        var indentX = 180;
        var indentY = 64;
        paper = InitializeRaphael(indentX, indentY);

        var currentY = 0;
        var parentNode = systemTree;
        var childNode = null;
        parentNode.parent = null;
        parentNode.x = 0;
        parentNode.y = 0;
        DrawSystem(paper, indentX, indentY, parentNode);
        while(parentNode != null) {
            if(childNode && !childNode.drawn) {
                DrawSystem(paper, indentX, indentY, childNode);
                childNode.drawn = true;
            }

            if(parentNode.children.length) {
                if(childNode) {
                    if(childNode.children && childNode.children.length &&
                        !childNode.children[0].drawn) {
                        parentNode = childNode;
                        childNode = childNode.children[0];
                        childNode.parent = parentNode;
                        childNode.index = 0;
                        childNode.x = parentNode.x + 1;
                        childNode.y = parentNode.y;
                    }
                    else if(childNode.index ==(parentNode.children.length - 1) &&
                             !parentNode.parent) {
                        parentNode = null;
                    }
                    else if(childNode.index ==(parentNode.children.length - 1) &&
                             parentNode.parent) {
                        childNode = parentNode;
                        parentNode = parentNode.parent;
                    }
                    else {
                        currentY++;
                        parentNode.children[childNode.index + 1].index = childNode.index + 1;
                        parentNode.children[childNode.index + 1].y = currentY;
                        parentNode.children[childNode.index + 1].x = childNode.x;
                        childNode = parentNode.children[childNode.index + 1];
                        childNode.parent = parentNode;
                    }
                }
                else {
                    childNode = parentNode.children[0];
                    childNode.parent = parentNode;
                    childNode.index = 0;
                    childNode.y = parentNode.y;
                    childNode.x = parentNode.x + 1;
                }
            }
            else {
                parentNode = parentNode.parent;
                childNode = null;
            }
        }
    }
});

function InitializeRaphael(indentX, indentY) {
    var canvasHeight = 80 + ((systemTreeWidth - 1) * indentY);
    var canvasWidth = 110 + ((systemTreeLength - 1) * indentX);
    return Raphael('systemsHolder', canvasWidth, canvasHeight);
}

function DrawSystem(paper, indentX, indentY, system) {
    if(system == null) return;

    var sysX = GetSystemX(indentX, system);
    var sysY = GetSystemY(indentY, system);

    var sysName = system.name;
    if(system.type != null && system.type.length > 0) sysName += "\n(" + system.type + ")";
    var sysText;

    if(system.x != null && system.x > 0) {
        system.ellipse = paper.ellipse(sysX, sysY, 45, 28);

        sysText = paper.text(sysX, sysY, sysName);
        sysText.ellipse = system.ellipse;

        ConnectSystems(paper, system.parent, system, "#825E48");
    }
    else {
        system.ellipse = paper.ellipse(sysX, sysY, 40, 30);

        sysText = paper.text(sysX, sysY, sysName);
        sysText.ellipse = system.ellipse;
    }
    system.ellipse.system = system;

    ColorSystem(system, sysText);

    system.ellipse.mouseover(OnSysOver);
    system.ellipse.mouseout(OnSysOut);
    system.ellipse.mousedown(OnSysDown);
    sysText.mouseover(OnSysOver);
    sysText.mouseout(OnSysOut);
    sysText.mousedown(OnSysDown);
}

function GetSystemX(indentX, system) {
    if(system) return 55 + indentX * system.x;
    else alert("system is null or undefined");
}

function GetSystemY(indentY, system) {
    if(system) return 40 + indentY * system.y;
    else alert("system is null or undefined");
}

function ColorSystem(system, sysText) {
    if(!system) {
        alert("system is null or undefined");
        return;
    }

    var sysColor = "#f00";
    var sysStroke = "#fff";
    var sysStrokeWidth = 2;
    var textFontSize = 12;
    var textColor = "#000";

    if(system.x < 1) {
        // root
        sysColor = "#A600A6";
        sysStroke = "#6A006A";
        textColor = "#fff";
        textFontSize = 14;
    }
    else {
        // not selected
        switch(system.type) {
            case "null":
                sysColor = "#CC0000";
                sysStroke = "#840000";
                textColor = "#fff";
                break;
            case "low":
                sysColor = "#93841E";
                sysStroke = "#7D5500";
                textColor = "#fff";
                break;
            case "high":
                sysColor = "#009F00";
                sysStroke = "#006600";
                textColor = "#fff";
                break;
            default:
                sysColor = "#F2F4FF";
                sysStroke = "#0657B9";
                textColor = "#0974EA";
                break;
        }
    }

    if(system.name.length > 16) textFontSize = 8;
    else if(system.name.length > 11) textFontSize = 9;

    system.ellipse.attr({fill: sysColor, stroke: sysStroke, "stroke-width": sysStrokeWidth, cursor: "pointer"});
    sysText.attr({fill: textColor, "font-size": textFontSize, cursor: "pointer"});
}

function ConnectSystems(paper, parentSystem, childSystem, lineColor) {
    var parentBox = parentSystem.ellipse.getBBox();
    var childBox = childSystem.ellipse.getBBox();
    var startY = parentBox.y + (parentBox.height / 2);
    var path;
    if(parentSystem.y == childSystem.y)
        path = paper.path("M" + parentBox.x2 + "," + startY + "L" + childBox.x + "," + startY);
    else {
        var endY = childBox.y + (childBox.height / 2);
        var parentControlX = parentBox.x2 + ((childBox.x - parentBox.x2) / 2);
        var childControlX = childBox.x - ((childBox.x - parentBox.x2) / 2);
        path = paper.path("M" + parentBox.x2 + "," + startY +
                          "C" + parentControlX + "," + startY + "," +
                          childControlX + "," + endY + "," +
                          childBox.x + "," + endY);
    }
    path.attr({stroke: lineColor});
}

function OnSysOver() {
    var ellipse;
    if(this.type == 'ellipse') ellipse = this;
    else ellipse = this.ellipse;
    var system = ellipse.system;

    ellipse.attr({"stroke-width": 4});

    if(!system.$infoPanel && !system.$actionPanel) {
        var ellipseBox = ellipse.getBBox();
        system.$infoPanel = $('#stash .system-info').clone().appendTo('#systemsHolder');
        system.$infoPanel.css({'top': ellipseBox.y, 'left': ellipseBox.x2});
        system.$infoPanel.children('#system-info-author').append(system.author);
        system.$infoPanel.children('#system-info-date').append(system.date);
        if(system.wspace_effect) {
            var $effectDiv = system.$infoPanel.children('#system-info-wspace-effect');
            $effectDiv.append(system.wspace_effect);
            $effectDiv.css('display', 'block');
        }
    }
}

function OnSysOut() {
    var ellipse;
    if(this.type == 'ellipse') ellipse = this;
    else ellipse = this.ellipse;
    var system = ellipse.system;

    if(system.$infoPanel) {
        ellipse.attr({"stroke-width": 2});
        system.$infoPanel.remove();
        system.$infoPanel = null;
    }
    else if(!system.$actionPanel) {
        ellipse.attr({"stroke-width": 2});
    }
}

function ClearSelection() {
    paper.forEach(function(el) {
        if(el.type == 'ellipse' && el.system.$actionPanel) {
            el.attr({"stroke-width": 2});
            el.system.$actionPanel.remove();
            el.system.$actionPanel = null;
        }
    });
}

function OnSysDown(e) {
    var ellipse;
    if(this.type == 'ellipse') ellipse = this;
    else ellipse = this.ellipse;
    var system = ellipse.system;

    if(system.$infoPanel) {
        ClearSelection();

        var $stashActionPanel = $('#stash .system-actions');
        system.$actionPanel = system.$infoPanel;
        system.$infoPanel = null;
        system.$actionPanel.attr('class', $stashActionPanel.attr('class'));
        system.$actionPanel.attr('data-ellipse-id', ellipse.id);
        system.$actionPanel.html($stashActionPanel.html());
    }
    else if(!system.$actionPanel) {
        ClearSelection();

        var ellipseBox = ellipse.getBBox();
        system.$actionPanel = $('#stash .system-actions').clone().appendTo('#systemsHolder');
        system.$actionPanel.css({'top': ellipseBox.y, 'left': ellipseBox.x2});
    }
}
