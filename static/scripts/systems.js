var paper;
var indentX = 180;
var indentY = 64;
var CANVAS_HEIGHT_PADDING = 80;
var CANVAS_WIDTH_PADDING = 110;
var ROOT_ELLIPSE_RX = 40;
var ROOT_ELLIPSE_RY = 30;
var NON_ROOT_ELLIPSE_RX = 45;
var NON_ROOT_ELLIPSE_RY = 28;
var SYSTEM_CONNECTION_LINE_COLOR = "#825E48";
var SYSTEM_PLACEHOLDER_NAME = 'XXX';

$(document).ready(function() {
    $('select').on('change', function() {
        if(this.value) {
            if(paper) ClearSelection();
            window.location = '/' + this.value;
        }
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

    if(typeof(systemTree) != 'undefined' && systemTree && systemTreeLength) {

        document.onclick = function(e) {
            var tag_name = e.target.tagName.toLowerCase();
            if(tag_name != 'ellipse' && tag_name != 'text' &&
               tag_name != 'tspan' && tag_name != 'path' && tag_name != 'a' &&
               !$(e.target).closest('form').length) {
                ClearSelection();
            }
        };

        document.onkeydown = function(e) {
            if(e.which == 27) ClearSelection();
        };

        function ReplaceActionPanelSystemAction(link, formClass) {
            var $stashSystemForm = $('#stash .' + formClass);
            var $container = $(link).parent();
            $container.html($stashSystemForm.html());
            $container.attr('class', $stashSystemForm.attr('class'));
            $container.find('#system-name').focus().autocomplete({
                select: function(event, ui) {
                    $(this).closest('form').find('input:submit')
                                           .removeAttr('disabled');
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
        }

        $('#systemsHolder').on('click', '#add-system', function(e) {
            e.preventDefault();
            ReplaceActionPanelSystemAction(this, 'new-system-form');
        });

        $('#systemsHolder').on('click', '#edit-system', function(e) {
            e.preventDefault();
            var $container = $(this).parent();
            ReplaceActionPanelSystemAction(this, 'edit-system-form');
            var system = paper.getById($container.attr('data-ellipse-id'))
                              .system;
            $container.find('#system-name').val(system.name);
            $container.find('#system-notes').val(system.notes_text);
        });

        $('#systemsHolder').on('click', '#add-connection', function(e) {
            e.preventDefault();

            var $stashConnectionForm = $('#stash .new-connection-form');
            var $container = $(this).parent();
            $container.html($stashConnectionForm.html());
            $container.attr('class', $stashConnectionForm.attr('class'));
            $container.find('#wormhole-sig').focus();
        });

        $('#systemsHolder').on('click', '#edit-connection', function(e) {
            e.preventDefault();

            var $stashConnectionForm = $('#stash .new-connection-form');
            var $container = $(this).parent();
            var connection = paper.getById($container.attr('data-path-id'))
                                  .connection;
            $container.html($stashConnectionForm.html());
            $container.attr('class',
                $stashConnectionForm.attr('class').replace('new', 'edit'));
            $container.find('#wormhole-sig').val(
                connection.wormhole_sig).focus();
            $container.find('#origin-celestial').val(
                connection.parent_celestial);
            $container.find('#destination-celestial').val(
                connection.child_celestial);
            $container.find('#life-level[value="' + connection.life_level +
                            '"]').attr('checked', true);
            $container.find('#mass-level[value="' + connection.mass_level +
                            '"]').attr('checked', true);
        });

        $('#systemsHolder').on('click', '#delete-system', function(e) {
            e.preventDefault();

            var nodeID = paper.getById($(this).parent().attr('data-ellipse-id'))
                              .system.id;
            $.ajax({
                type: 'DELETE',
                url: '/api/system_node/' +
                     window.location.pathname.split('/')[1] + '/' + nodeID +
                     '/',
                success: function() {
                    if(nodeID == systemTree.id) window.location = '/';
                    else {
                        ClearSelection(true);
                        DeleteNode(nodeID);
                    }
                },
                error: function(xhr) {
                    alert(xhr.responseText);
                }
            });
        });

        $('#systemsHolder').on('submit', '.new-system-form', function(e) {
            e.preventDefault();

            var $formDiv = $(this);

            var systemName = $formDiv.find('#system-name').val().trim();
            if($formDiv.find('input:submit:disabled').length ||
               systemName == '') {
                alert('A valid system name must be entered.');
                return;
            }

            $.ajax({
                type: 'POST',
                url: '/api/system_node/',
                data: {
                    'system': systemName,
                    'page_name': window.location.pathname.split('/')[1],
                    'parent_node': paper.getById(
                        $formDiv.attr('data-ellipse-id')).system.id
                },
                success: function(data) {
                    ClearSelection(true);
                    AddNode(JSON.parse(data));
                },
                error: function(xhr) {
                    alert(xhr.responseText);
                }
            });
        });

        $('#systemsHolder').on('submit', '.edit-system-form', function(e) {
            e.preventDefault();

            var $formDiv = $(this);

            var systemName = $formDiv.find('#system-name').val().trim();
            if($formDiv.find('input:submit:disabled').length ||
               systemName == '') {
                alert('A valid system name must be entered.');
                return;
            }

            $.ajax({
                type: 'PUT',
                url: '/api/system_node/' +
                     window.location.pathname.split('/')[1] + '/' +
                     paper.getById($formDiv.attr('data-ellipse-id')).system.id +
                     '/',
                data: {
                    'system': systemName,
                    'notes': $formDiv.find('#system-notes').val()
                },
                success: function(data) {
                    ClearSelection(true);
                    UpdateNode(JSON.parse(data));
                },
                error: function(xhr) {
                    alert(xhr.responseText);
                }
            });
        });

        $('#systemsHolder').on('submit', '.new-connection-form', function(e) {
            e.preventDefault();

            var $formDiv = $(this);

            var wormholeSig = $formDiv.find('#wormhole-sig').val().trim();
            if(wormholeSig == '' || wormholeSig.length != WORMHOLE_SIG_LENGTH) {
                alert('A valid wormhole sig must be entered.');
                return;
            }

            var $lifeLevel = $formDiv.find('#life-level:checked');
            if(!$lifeLevel.length) {
                alert('A life level must be selected.');
                return;
            }

            var $massLevel = $formDiv.find('#mass-level:checked');
            if(!$massLevel.length) {
                alert('A mass level must be selected.');
                return;
            }

            $.ajax({
                type: 'POST',
                url: '/api/system_connection/',
                data: {
                    'wormhole': wormholeSig,
                    'parent_celestial':
                        $formDiv.find('#origin-celestial').val().trim(),
                    'child_celestial':
                        $formDiv.find('#destination-celestial').val().trim(),
                    'life_level': $lifeLevel.val(),
                    'mass_level': $massLevel.val(),
                    'parent_node': paper.getById(
                        $formDiv.attr('data-ellipse-id')).system.id,
                    'page_name': window.location.pathname.split('/')[1]
                },
                success: function(data) {
                    ClearSelection(true);
                    AddNode(JSON.parse(data));
                },
                error: function(xhr) {
                    alert(xhr.responseText);
                }
            });
        });

        $('#systemsHolder').on('submit', '.edit-connection-form', function(e) {
            e.preventDefault();

            var $formDiv = $(this);

            var wormholeSig = $formDiv.find('#wormhole-sig').val().trim();
            if(wormholeSig == '' || wormholeSig.length != WORMHOLE_SIG_LENGTH) {
                alert('A valid wormhole sig must be entered.');
                return;
            }

            var $lifeLevel = $formDiv.find('#life-level:checked');
            if(!$lifeLevel.length) {
                alert('A life level must be selected.');
                return;
            }

            var $massLevel = $formDiv.find('#mass-level:checked');
            if(!$massLevel.length) {
                alert('A mass level must be selected.');
                return;
            }

            $.ajax({
                type: 'PUT',
                url: '/api/system_connection/' +
                    paper.getById($formDiv.attr('data-path-id')).connection.id +
                    '/',
                data: {
                    'wormhole': wormholeSig,
                    'parent_celestial':
                        $formDiv.find('#origin-celestial').val().trim(),
                    'child_celestial':
                        $formDiv.find('#destination-celestial').val().trim(),
                    'life_level': $lifeLevel.val(),
                    'mass_level': $massLevel.val()
                },
                success: function(data) {
                    ClearSelection(true);
                    UpdateConnection(JSON.parse(data));
                },
                error: function(xhr) {
                    alert(xhr.responseText);
                }
            });
        });

        paper = Raphael('systemsHolder', getCanvasWidth(), getCanvasHeight());

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
                    if(childNode.children.length &&
                       !childNode.children[0].drawn) {
                        parentNode = childNode;
                        childNode = childNode.children[0];
                        childNode.parent = parentNode;
                        childNode.index = 0;
                        childNode.x = parentNode.x + 1;
                        childNode.y = parentNode.y;
                    }
                    else if(
                        childNode.index == (parentNode.children.length - 1) &&
                        !parentNode.parent) {
                        parentNode = null;
                    }
                    else if(
                        childNode.index == (parentNode.children.length - 1) &&
                        parentNode.parent) {
                        childNode = parentNode;
                        parentNode = parentNode.parent;
                    }
                    else {
                        currentY++;
                        parentNode.children[childNode.index + 1].index =
                            childNode.index + 1;
                        parentNode.children[childNode.index + 1].y = currentY;
                        parentNode.children[childNode.index + 1].x =
                            childNode.x;
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

        if(objectLocks) {
            objectLocks.forEach(function(objectLock) {
                paper.forEach(function(el) {
                    if(objectLock.type == 'node' && el.type == 'ellipse' &&
                       el.system.id == objectLock.id) {
                        LockNode(el, objectLock.username);
                        return;
                    }
                    else if(objectLock.type == 'connection' &&
                            el.type == 'path' && el.connection &&
                            el.connection.id == objectLock.id) {
                        LockConnection(el, objectLock.username);
                        return;
                    }
                });
            });
        }
    }

    GetUpdates();
});

function getCanvasWidth() {
    return CANVAS_WIDTH_PADDING + ((systemTreeLength - 1) * indentX);
}

function getCanvasHeight() {
    return CANVAS_HEIGHT_PADDING + ((systemTreeWidth - 1) * indentY);
}

function DrawSystem(paper, indentX, indentY, system) {
    if(system == null) return;

    var systemX = GetSystemX(indentX, system);
    var systemY = GetSystemY(indentY, system);

    var systemName = system.name;
    if(!systemName) systemName = SYSTEM_PLACEHOLDER_NAME;

    if(system.type && system.type.length > 0)
        systemName += "\n(" + system.type + ")";

    var systemText;
    if(system.x > 0) {
        system.ellipse = paper.ellipse(systemX, systemY, NON_ROOT_ELLIPSE_RX,
                                       NON_ROOT_ELLIPSE_RY);
        systemText = paper.text(systemX, systemY, systemName);
        ConnectSystems(paper, system.parent, system,
                       SYSTEM_CONNECTION_LINE_COLOR);
    }
    else {
        system.ellipse = paper.ellipse(systemX, systemY, ROOT_ELLIPSE_RX,
                                       ROOT_ELLIPSE_RY);
        systemText = paper.text(systemX, systemY, systemName);
    }
    system.ellipse.text = systemText;
    systemText.ellipse = system.ellipse;
    system.ellipse.system = system;

    ColorSystem(system, systemText);

    system.ellipse.mouseover(OnSystemHover);
    system.ellipse.mouseout(OnSystemHoverOut);
    system.ellipse.mousedown(OnSystemClick);
    systemText.mouseover(OnSystemHover);
    systemText.mouseout(OnSystemHoverOut);
    systemText.mousedown(OnSystemClick);
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

    if(system.name) {
        if(system.name.length > 16) textFontSize = 8;
        else if(system.name.length > 11) textFontSize = 9;
    }

    system.ellipse.attr({'fill' : sysColor, 'stroke' : sysStroke,
                        'stroke-width' : sysStrokeWidth, 'cursor' : "pointer"});
    sysText.attr({'fill' : textColor, 'font-size' : textFontSize,
                  'cursor' : "pointer"});
}

function ConnectSystems(paper, parentSystem, childSystem, lineColor) {
    var parentBox = parentSystem.ellipse.getBBox();
    var childBox = childSystem.ellipse.getBBox();
    var startY = parentBox.y + (parentBox.height / 2);
    var path;
    if(parentSystem.y == childSystem.y)
        path = paper.path("M" + parentBox.x2 + "," + startY + "L" + childBox.x +
                          "," + startY);
    else {
        var endY = childBox.y + (childBox.height / 2);
        var parentControlX = parentBox.x2 + ((childBox.x - parentBox.x2) / 2);
        var childControlX = childBox.x - ((childBox.x - parentBox.x2) / 2);
        path = paper.path("M" + parentBox.x2 + "," + startY +
                          "C" + parentControlX + "," + startY + "," +
                          childControlX + "," + endY + "," +
                          childBox.x + "," + endY);
    }
    path.attr('stroke', lineColor);
    path.childNode = childSystem.ellipse;
    path.connection = childSystem.parent_connection;
    path.mousedown(OnConnectionClick);
    childSystem.ellipse.pathToParent = path;
}

function OnSystemHover() {
    var ellipse;
    if(this.type == 'ellipse') ellipse = this;
    else ellipse = this.ellipse;
    var system = ellipse.system;

    ellipse.attr('stroke-width', 4);

    if(!system.$infoPanel && !system.$actionPanel) {
        var ellipseBox = ellipse.getBBox();
        system.$infoPanel = $('#stash .system-info').clone()
                                                    .appendTo('#systemsHolder');
        system.$infoPanel.css({'top': ellipseBox.y, 'left': ellipseBox.x2});
        system.$infoPanel.children('#system-info-author').append(system.author);
        system.$infoPanel.children('#system-info-date').append(system.date);
        if(system.wspace_effect)
            system.$infoPanel.children('#system-info-wspace-effect')
                             .append(system.wspace_effect)
                             .removeAttr('hidden');
        if(system.notes_text)
            system.$infoPanel.children('#system-info-notes')
                             .append(system.notes_html)
                             .removeAttr('hidden');
        if(system.locked)
            system.$infoPanel.children('#system-info-lock')
                             .append(system.locked)
                             .removeAttr('hidden');
    }
}

function OnSystemHoverOut() {
    var ellipse;
    if(this.type == 'ellipse') ellipse = this;
    else ellipse = this.ellipse;
    var system = ellipse.system;

    if(system.$infoPanel) {
        if(!system.locked) ellipse.attr('stroke-width', 2);
        system.$infoPanel.remove();
        system.$infoPanel = null;
    }
    else if(!system.$actionPanel) {
        if(!system.locked) ellipse.attr('stroke-width', 2);
    }
}

function ClearSelection(softClear) {
    paper.forEach(function(el) {
        if((el.type == 'ellipse' && el.system.$actionPanel) ||
           (el.type == 'path' && el.connection && el.connection.$actionPanel)) {
            if(!softClear) {
                $.ajax({
                    type: 'POST',
                    url: '/lock_object/',
                    data: {
                        'node_id' : null,
                        'page_name': window.location.pathname.split('/')[1]
                    }
                });
            }
            if(el.type == 'ellipse') {
                el.attr('stroke-width', 2);
                el.system.$actionPanel.remove();
                el.system.$actionPanel = null;
            }
            else {
                el.connection.$actionPanel.remove();
                el.connection.$actionPanel = null;
            }
            return;
        }
    });
}

function ActivateNode(system, ellipse) {
    if(system.$infoPanel) {
        ClearSelection(true);

        var $stashActionPanel = $('#stash .system-actions');
        system.$actionPanel = system.$infoPanel;
        system.$infoPanel = null;
        system.$actionPanel.attr('class', $stashActionPanel.attr('class'));
        system.$actionPanel.attr('data-ellipse-id', ellipse.id);
        system.$actionPanel.html($stashActionPanel.html());
    }
    else if(!system.$actionPanel) {
        ClearSelection(true);

        var ellipseBox = ellipse.getBBox();
        system.$actionPanel = $('#stash .system-actions').clone()
                              .appendTo('#systemsHolder');
        system.$actionPanel.css({'top': ellipseBox.y, 'left': ellipseBox.x2});
    }
}

function OnSystemClick() {
    var ellipse;
    if(this.type == 'ellipse') ellipse = this;
    else ellipse = this.ellipse;
    var system = ellipse.system;

    if(!system.locked && !system.$actionPanel) {
        if(system.children.length) {
            var checkedDescendants = [];
            var currentNode = system;
            while(currentNode) {
                if(system.children.length &&
                   checkedDescendants.indexOf(system.children[0].id) == -1)
                    currentNode = system.children[0];
                else
                    currentNode = TraverseToNextNode(currentNode);

                if(currentNode.id == system.id) break;

                if(currentNode.locked || (currentNode.pathToParent &&
                    currentNode.pathToParent.connection &&
                    currentNode.pathToParent.connection.locked)) {
                    alert('Cannot lock a node whose descendant is locked.');
                    return;
                }

                checkedDescendants.push(currentNode.id);
                if(currentNode.pathToParent &&
                   currentNode.pathToParent.connection)
                    checkedDescendants.push(
                        currentNode.pathToParent.connection.id);
            }
        }

        $.ajax({
            type: 'POST',
            url: '/lock_object/',
            data: {
                'node_id' : system.id,
                'page_name': window.location.pathname.split('/')[1]
            },
            success: function() {
                ActivateNode(system, ellipse);
            },
            error: function(xhr, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
    }
}

function OnConnectionClick() {
    if(this.connection && !this.connection.locked &&
       !this.connection.$actionPanel) {
        var path = this;
        $.ajax({
            type: 'POST',
            url: '/lock_object/',
            data: {
                'connection_id' : path.connection.id,
                'page_name': window.location.pathname.split('/')[1]
            },
            success: function() {
                ClearSelection(true);
                var pathBox = path.getBBox();
                path.connection.$actionPanel =
                    $('#stash .connection-actions').clone()
                    .appendTo('#systemsHolder');
                path.connection.$actionPanel.attr('data-path-id', path.id);
                path.connection.$actionPanel.css(
                    {'top': pathBox.y, 'left': pathBox.x2});
            },
            error: function(xhr, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
    }
}

function TraverseToNextNode(currentNode) {
    if(!currentNode.parent)
        return currentNode;
    else if(currentNode.index < (currentNode.parent.children.length - 1))
        return currentNode.parent.children[currentNode.index + 1];
    else
        return currentNode.parent;
}

function LockNode(ellipse, username, noTraversal) {
    var currentNode = ellipse.system;
    currentNode.ellipse.attr({'stroke-width': 4, 'fill': 'gray'});
    currentNode.locked = username;
    if(!noTraversal) {
        if(ellipse.pathToParent && ellipse.pathToParent.connection)
            ellipse.pathToParent.connection.locked = username;
        if(currentNode.children.length) {
            while(currentNode) {
                if(currentNode.children.length &&
                   !currentNode.children[0].locked)
                    currentNode = currentNode.children[0];
                else
                    currentNode = TraverseToNextNode(currentNode);
                if(currentNode.id == ellipse.system.id) break;
                if(!currentNode.locked) {
                    currentNode.ellipse.attr({'stroke-width': 4,
                                              'fill': 'gray'});
                    currentNode.locked = username;
                    if(currentNode.ellipse.pathToParent &&
                       currentNode.ellipse.pathToParent.connection)
                        LockConnection(currentNode.ellipse.pathToParent,
                                       username, true);
                }
            }
        }
    }
}

function UnlockNode(ellipse, noTraversal) {
    var currentNode = ellipse.system;
    var locker = currentNode.locked;
    ColorSystem(currentNode, currentNode.ellipse.text);
    currentNode.locked = null;
    if(!noTraversal && currentNode.children.length) {
        while(currentNode) {
            if(currentNode.children.length && currentNode.children[0].locked)
                currentNode = currentNode.children[0];
            else
                currentNode = TraverseToNextNode(currentNode);
            if(currentNode.id == ellipse.system.id) break;
            if(currentNode.locked && currentNode.locked == locker) {
                ColorSystem(currentNode, currentNode.ellipse.text);
                currentNode.locked = null;
                if(currentNode.ellipse.pathToParent &&
                   currentNode.ellipse.pathToParent.connection)
                    UnlockConnection(currentNode.ellipse.pathToParent);
            }
        }
    }
}

function LockConnection(path, username, noTraversal) {
    path.connection.locked = username;
    if(!noTraversal) LockNode(path.childNode, username, true);
}

function UnlockConnection(path) {
    path.connection.locked = null;
    UnlockNode(path.childNode, true);
}

function AddNode(node) {
    paper.forEach(function(elem) {
        if(elem.type == 'ellipse' && elem.system.id == node.parent_node_id) {
            node.parent = elem.system;
            node.x = elem.system.x + 1;
            if(elem.system.children.length) {
                systemTreeWidth++;
                paper.setSize(paper.width, getCanvasHeight());

                var nodeChainY = elem.system.children[
                    elem.system.children.length - 1].y;
                var currentNode = elem.system;
                while(currentNode) {
                    if(currentNode.y > nodeChainY) nodeChainY = currentNode.y;
                    if(currentNode.children.length)
                        currentNode = currentNode.children[
                            currentNode.children.length - 1];
                    else currentNode = null;
                }
                node.y = nodeChainY + 1;

                paper.forEach(function(el) {
                    if(el.type == 'ellipse' && el.system.y >= node.y) {
                        el.system.y++;
                        el.transform('...t0,' + indentY);
                        el.text.transform('...t0,' + indentY);
                        if(el.system.x < node.x &&
                           el.system.parent.y < node.y &&
                           el.pathToParent.attrs.path[1][0] == 'C') {
                            el.pathToParent.attrs.path[1][4] =
                                el.pathToParent.attrs.path[1][4] + indentY;
                            el.pathToParent.attrs.path[1][6] =
                                el.pathToParent.attrs.path[1][6] + indentY;
                            el.pathToParent.attr('path',
                                el.pathToParent.attrs.path[0].join() +
                                el.pathToParent.attrs.path[1].join());
                        }
                        else el.pathToParent.transform('...t0,' + indentY);
                    }
                });
            }
            else {
                var distanceToRoot = 0;
                var currentNode = elem.system;
                while(currentNode) {
                    currentNode = currentNode.parent;
                    distanceToRoot++;
                }
                if(distanceToRoot == systemTreeLength) {
                    systemTreeLength++;
                    paper.setSize(getCanvasWidth(), paper.height);
                }
                node.y = elem.system.y;
            }
            node.index = node.parent.children.length;
            elem.system.children.push(node);
            DrawSystem(paper, indentX, indentY, node);

            return;
        }
    });
}

function DeleteNode(nodeID) {
    paper.forEach(function(el) {
        if(el.type == 'ellipse' && el.system.id == nodeID) {
            var currentNode = el.system;
            var nodeChainWidth = 1;
            while(currentNode) {
                if(currentNode.children.length)
                    currentNode = currentNode.children[0];
                else {
                    if((currentNode.y - el.system.y + 1) > nodeChainWidth)
                        nodeChainWidth = currentNode.y - el.system.y + 1;

                    currentNode.ellipse.pathToParent.remove();
                    currentNode.ellipse.text.remove();
                    currentNode.ellipse.remove();

                    if(currentNode.id == nodeID) {
                        if(currentNode.y == currentNode.parent.y &&
                           currentNode.parent.children.length == 1)
                            nodeChainWidth--;

                        for(var i = currentNode.index + 1;
                            i < currentNode.parent.children.length; i++) {
                            currentNode.parent.children[i].index--;
                        }
                        currentNode.parent.children.splice(currentNode.index,
                                                           1);

                        if(nodeChainWidth) {
                            paper.forEach(function(elem) {
                                if(elem.type == 'ellipse' &&
                                   elem.system.y > currentNode.y) {
                                    if((elem.system.x < currentNode.x ||
                                           (elem.system.x == currentNode.x &&
                                               elem.system.parent.id ==
                                               currentNode.parent.id)) &&
                                       elem.system.parent.y <= currentNode.y &&
                                       elem.pathToParent.attrs.path[1][0] ==
                                       'C') {
                                        if(elem.system.index) {
                                            elem.pathToParent.attrs.path[1][4] =
                                                elem.pathToParent.attrs
                                                    .path[1][4] -
                                                (indentY * nodeChainWidth);
                                            elem.pathToParent.attrs.path[1][6] =
                                                elem.pathToParent.attrs
                                                    .path[1][6] -
                                                (indentY * nodeChainWidth);
                                            elem.pathToParent.attr('path',
                                                elem.pathToParent.attrs.path[0]
                                                    .join() +
                                                elem.pathToParent.attrs.path[1]
                                                    .join());
                                        }
                                        else {
                                            elem.pathToParent.attr('path',
                                                elem.pathToParent.attrs.path[0]
                                                    .join() +
                                                'L' + elem.pathToParent.attrs
                                                          .path[1][5] +
                                                ',' + elem.pathToParent.attrs
                                                          .path[0][2]);
                                        }
                                    }
                                    else
                                        elem.pathToParent.transform('...t0,-' +
                                            (indentY * nodeChainWidth));

                                    elem.system.y -= nodeChainWidth;
                                    elem.transform('...t0,-' +
                                        (indentY * nodeChainWidth));
                                    elem.text.transform('...t0,-' +
                                        (indentY * nodeChainWidth));
                                }
                            });
                        }

                        currentNode = null;
                    }
                    else {
                        currentNode = currentNode.parent;
                        currentNode.children.splice(0,1);
                    }
                }
            }

            return;
        }
    });

    var maxX = 0;
    var maxY = 0;
    paper.forEach(function(el) {
        if(el.type == 'ellipse') {
            if(el.system.x > maxX) maxX = el.system.x;
            if(el.system.y > maxY) maxY = el.system.y;
        }
    });
    if(maxX < (systemTreeLength - 1)) systemTreeLength = maxX + 1;
    if(maxY < (systemTreeWidth - 1)) systemTreeWidth = maxY + 1;
    paper.setSize(getCanvasWidth(), getCanvasHeight());
}

function UpdateNode(node) {
    paper.forEach(function(el) {
        if(el.type == 'ellipse' && el.system.id == node.id) {
            el.system.author = node.author;
            el.system.date = node.date;
            if(el.system.name != node.name) {
                el.system.name = node.name;
                el.text.attr('text', node.name + '\n(' + node.type + ')');
                if(el.system.type != node.type) {
                    el.system.type = node.type;
                    ColorSystem(el.system, el.text);
                }
                el.system.region = node.region;
            }
            el.system.notes_text = node.notes_text;
            el.system.notes_html = node.notes_html;
            return;
        }
    });
}

function UpdateConnection(connection) {
    paper.forEach(function(el) {
        if(el.type == 'ellipse' && el.pathToParent &&
           el.pathToParent.connection &&
           el.pathToParent.connection.id == connection.id) {
            var curConnection = el.pathToParent.connection;
            curConnection.author = connection.author;
            curConnection.parent_celestial = connection.parent_celestial;
            curConnection.child_celestial = connection.child_celestial;
            curConnection.life_level = connection.life_level;
            curConnection.mass_level = connection.mass_level;
            if(curConnection.wormhole_sig != connection.wormhole_sig) {
                curConnection.wormhole_sig = connection.wormhole_sig;
                if(!el.system.name && curConnection.facing_down &&
                   connection.wormhole_type &&
                   el.system.type != connection.wormhole_type) {
                    el.system.type = connection.wormhole_type;
                    el.text.attr('text', SYSTEM_PLACEHOLDER_NAME + '\n(' +
                                 el.system.type + ')');
                    ColorSystem(el.system, el.text);
                }
            }
            return;
        }
    });
}

function GetUpdates() {
    $.ajax({
        type: "GET",
        url: "/get_updates/" + window.location.pathname.split('/')[1] + "/",
        success: function(data) {
            $('#user-list').html(data.user_list.join(', '));

            if(data.object_lock) {
                if(data.object_lock.username) {
                    paper.forEach(function(el) {
                        if(el.type == 'ellipse' && el.system.locked &&
                           el.system.locked == data.object_lock.username)
                            UnlockNode(el);
                        else if(el.type == 'path' && el.connection &&
                                el.connection.locked &&
                                el.connection.locked ==
                                data.object_lock.username)
                            UnlockConnection(el);
                    });
                }
                paper.forEach(function(el) {
                    if(data.object_lock.type == 'node' &&
                       el.type == 'ellipse' &&
                       el.system.id == data.object_lock.id) {
                        if(data.object_lock.username)
                            LockNode(el, data.object_lock.username);
                        else
                            UnlockNode(el);
                        return;
                    }
                    else if(data.object_lock.type == 'connection' &&
                            el.type == 'path' && el.connection &&
                            el.connection.id == data.object_lock.id) {
                        if(data.object_lock.username)
                            LockConnection(el, data.object_lock.username);
                        else
                            UnlockConnection(el);
                        return;
                    }
                });
            }

            if(data.new_page) {
                $('select').append('<option value="' + data.new_page + '">' +
                                   data.new_page + '</option>');
            }
            else if(data.delete_page) {
                if(window.location.pathname == ('/' + data.delete_page)) {
                    window.location = '/';
                    return;
                }
                else
                    $('select').find('option[value="' + data.delete_page + '"]')
                               .remove();
            }
            else if(data.new_node)
                AddNode(data.new_node);
            else if(data.delete_node)
                DeleteNode(data.delete_node);
            else if(data.update_node)
                UpdateNode(data.update_node);
            else if(data.update_connection)
                UpdateConnection(data.update_connection);

            window.setTimeout(GetUpdates, 0);
        },
        error: function(xhr, textStatus, errorThrown) {
            alert(errorThrown);
        }
    });
}
