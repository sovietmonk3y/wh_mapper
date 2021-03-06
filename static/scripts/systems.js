var paper;
var VERTICAL_LEVEL_OFFSET = 10;
var RECT_WIDTH = 140;
var RECT_HEIGHT = 50;
var PARENT_CONNECTION_SQUARE_OFFSET = 10;
var CHILD_CONNECTION_SQUARE_OFFSET = 20;
var CONNECTION_SQUARE_SIZE = 50;
var CONNECTION_TRIANGLE_WIDTH = 10;
var CONNECTION_TRIANGLE_HEIGHT = 5;
var CONNECTION_SQUARE_PATH_OFFSET = 10;
var CONNECTION_SQUARE_TEXT_OFFSET = 30;
var CONNECTION_PATH_TEXT_VERTICAL_OFFSET = 10;
var CONNECTION_PATH_LENGTH = 100;
var SYSTEM_PLACEHOLDER_NAME = '?';

var KG_TO_MILKG = 1000000;

var PARENT_CHILD_HORIZONTAL_OFFSET = PARENT_CONNECTION_SQUARE_OFFSET +
    (CONNECTION_SQUARE_SIZE * 2) + (CONNECTION_SQUARE_PATH_OFFSET * 2) +
    CONNECTION_PATH_LENGTH + CHILD_CONNECTION_SQUARE_OFFSET;

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
            var tagName = e.target.tagName.toLowerCase();
            if(tagName == 'svg' || tagName == 'body') ClearSelection();
        };

        document.onkeydown = function(e) {
            if(e.which == 27) ClearSelection();
        };

        $('#map').on('keyup', '#system-name', function(e) {
            if(e.target.value == '')
                $(this).closest('form').find('input:submit').attr('disabled',
                    true);
        });

        function ActivateSystemActionModal(system, formClass) {
            var $container = $('#stash .' + formClass).clone().dialog({
                appendTo: '#map',
                modal: true,
                close: function(e) {
                    $(e.target).dialog('destroy');
                }
            });

            $container[0].system = system;

            $container.find('#system-name').autocomplete({
                select: function() {
                    $(this).closest('form').find('input:submit').removeAttr(
                        'disabled');
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

            return $container;
        }

        $('#map').on('click', '.new-object-choice #gate', function() {
            var $container = $(this).parent();
            var system = $container[0].system;
            $container.dialog('destroy');
            ActivateSystemActionModal(system, 'new-system-form');
        });

        $('#map').on('click', '.new-object-choice #wormhole', function() {
            var $container = $(this).parent();
            var system = $container[0].system;
            $container.dialog('destroy');
            ActivateSystemActionModal(system, 'new-connection-form');
        });

        function ActivateSystemAdditionModal(button) {
            var $container = $('#stash .new-object-choice').clone().dialog({
                appendTo: '#map',
                modal: true,
                close: function(e) {
                    $(e.target).dialog('destroy');
                }
            });

            $container.children('#gate').focus();

            $container[0].system = button.parentElement.system;
        }

        $('#map').on('click', '.system-action-overlay #add', function() {
            ActivateSystemAdditionModal(this);
        });

        $('#map').on('click', '.system-action-overlay #edit', function() {
            var system = this.parentElement.system;
            var $formDiv = ActivateSystemActionModal(system,
                'edit-system-form');
            $formDiv.find('#system-name').val(system.name);
            $formDiv.find('#system-notes').val(system.notes_text);
        });

        $('#map').on('click', '.system-action-overlay #delete', function() {
            var nodeID = this.parentElement.system.id;
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

        $('#map').on('submit', '.new-system-form', function(e) {
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
                    'parent_node': $formDiv[0].system.id
                },
                success: function(data) {
                    $formDiv.dialog('destroy');
                    ClearSelection(true);
                    AddNode(JSON.parse(data));
                },
                error: function(xhr) {
                    alert(xhr.responseText);
                }
            });
        });

        $('#map').on('submit', '.edit-system-form', function(e) {
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
                     $formDiv[0].system.id + '/',
                data: {
                    'system': systemName,
                    'notes': $formDiv.find('#system-notes').val()
                },
                success: function(data) {
                    $formDiv.dialog('destroy');
                    ClearSelection(true);
                    UpdateNode(JSON.parse(data));
                },
                error: function(xhr) {
                    alert(xhr.responseText);
                }
            });
        });

        $('#map').on('submit', '.new-connection-form', function(e) {
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
                    'parent_node': $formDiv[0].system.id,
                    'page_name': window.location.pathname.split('/')[1]
                },
                success: function(data) {
                    $formDiv.dialog('destroy');
                    ClearSelection(true);
                    AddNode(JSON.parse(data));
                },
                error: function(xhr) {
                    alert(xhr.responseText);
                }
            });
        });

        $('#map').on('click', '.connection-action-overlay .edit', function() {
            var $container = $('#stash .new-connection-form').clone().dialog({
                appendTo: '#map',
                modal: true,
                close: function(e) {
                    $(e.target).dialog('destroy');
                }
            });
            $container.attr('class', $container.attr('class').replace('new',
                'edit'));

            var connection = this.parentElement.connection;
            $container.find('#wormhole-sig').val(connection.wormhole.sig);
            $container.find('#origin-celestial').val(
                connection.parent_celestial);
            $container.find('#destination-celestial').val(
                connection.child_celestial);
            $container.find('#life-level[value="' + connection.life_level +
                '"]').attr('checked', true);
            $container.find('#mass-level[value="' + connection.mass_level +
                '"]').attr('checked', true);

            $container[0].connection = connection;
        });

        $('#map').on('submit', '.edit-connection-form', function(e) {
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
                url: '/api/system_connection/' + $formDiv[0].connection.id +
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
                    $formDiv.dialog('destroy');
                    ClearSelection(true);
                    UpdateConnection(JSON.parse(data));
                },
                error: function(xhr) {
                    alert(xhr.responseText);
                }
            });
        });

        paper = Raphael('map', getCanvasWidth(), getCanvasHeight());

        var currentY = 0;
        var parentNode = systemTree;
        var childNode = null;
        parentNode.parent = null;
        parentNode.x = 0;
        parentNode.y = 0;
        DrawSystem(paper, parentNode);
        while(parentNode != null) {
            if(childNode && !childNode.drawn) {
                DrawSystem(paper, childNode);
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
                    if(objectLock.type == 'node' && el.type == 'rect' &&
                       el.system && el.system.id == objectLock.id) {
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
    return (RECT_WIDTH * systemTreeLength) +
        ((systemTreeLength - 1) * PARENT_CHILD_HORIZONTAL_OFFSET);
}

function getCanvasHeight() {
    return (RECT_HEIGHT * systemTreeWidth) +
        ((systemTreeWidth - 1) * VERTICAL_LEVEL_OFFSET);
}

function GetSystemText(system) {
    var text = system.name;
    if(!text) text = SYSTEM_PLACEHOLDER_NAME;

    text += "\n";
    if(system.region)
        text += system.region;
    else if(system.type && system.type.length == 2)
        text += system.type;
    else
        text += SYSTEM_PLACEHOLDER_NAME;

    return text;
}

function DrawSystem(paper, system) {
    if(system == null) return;

    var systemX = GetSystemX(system);
    var systemY = GetSystemY(system);

    system.rect = paper.rect(systemX, systemY, RECT_WIDTH, RECT_HEIGHT);

    if(system.x > 0) ConnectSystems(paper, system.parent, system);

    var systemText = paper.text(systemX + (RECT_WIDTH / 2),
        systemY + (RECT_HEIGHT / 2), GetSystemText(system));

    system.rect.text = systemText;
    systemText.rect = system.rect;
    system.rect.system = system;

    ColorSystem(system);

    system.rect.mouseover(OnSystemHover);
    system.rect.mouseout(OnSystemHoverOut);
    system.rect.mousedown(OnSystemClick);
    systemText.mouseover(OnSystemHover);
    systemText.mouseout(OnSystemHoverOut);
    systemText.mousedown(OnSystemClick);
}

function GetSystemX(system) {
    return (RECT_WIDTH + PARENT_CHILD_HORIZONTAL_OFFSET) * system.x;
}

function GetSystemY(system) {
    return (RECT_HEIGHT + VERTICAL_LEVEL_OFFSET) * system.y;
}

function ColorSystem(system) {
    system.rect.node.setAttribute('class', system.type);
}

function GetParentConnRectText(connection) {
    var text;
    if(connection.facing_down) {
        text = connection.wormhole.sig;
        if(connection.wormhole.static) text += ' (S)';
    }
    else text = 'K162';

    if(connection.parent_celestial) text += '\nP' + connection.parent_celestial;

    return text;
}

function GetChildConnRectText(connection) {
    var text;
    if(connection.facing_down) text = 'K162';
    else {
        if(connection.wormhole.sig == 'K162') text = '?';
        else {
            text = connection.wormhole.sig;
            if(connection.wormhole.static) text += ' (S)';
        }
    }

    if(connection.child_celestial) text += '\nP' + connection.child_celestial;

    return text;
}

function GetConnectionLifeText(connection) {
    var text;
    if(connection.wormhole.sig == 'K162') text = '?';
    else {
        var connectionDate = new Date(connection.date);
        var utcHours = connectionDate.getHours();
        connectionDate.setHours(0);
        connectionDate = connectionDate.setUTCHours(utcHours);
        var dateDiffHours = ((Date.now() - connectionDate) /
                             (1000 * 60 * 60)).toFixed();
        switch(connection.life_level) {
            case 0:
                if(connection.wormhole.life - dateDiffHours > 0)
                    text = '~' + (connection.wormhole.life - dateDiffHours);
                break;
            case 1:
                if((connection.wormhole.life * 0.25) - dateDiffHours > 0)
                    text = '>' + ((connection.wormhole.life * 0.25) -
                        dateDiffHours);
                break;
            case 2:
                if((connection.wormhole.life * 0.25) - dateDiffHours > 0)
                    text = '<' + ((connection.wormhole.life * 0.25) -
                        dateDiffHours);
                break;
        }
        if(text) text += 'hr';
        else text = 'DEAD';
    }
    return text;
}

function GetConnectionJumpMassText(connection) {
    if(connection.wormhole.sig == 'K162') return '?';
    else return (connection.wormhole.jump_mass / KG_TO_MILKG) + 'jmp';
}

function GetConnectionMassText(connection) {
    var text;
    if(connection.wormhole.sig == 'K162') text = '?';
    else {
        switch(connection.mass_level) {
            case 0:
                text = ((connection.wormhole.total_mass * 0.5) / KG_TO_MILKG) +
                    '-' + (connection.wormhole.total_mass / KG_TO_MILKG);
                break;
            case 1:
                text = ((connection.wormhole.total_mass * 0.1) / KG_TO_MILKG) +
                    '-' + ((connection.wormhole.total_mass * 0.5) /
                    KG_TO_MILKG);
                break;
            case 2:
                text = '0-' + ((connection.wormhole.total_mass * 0.1) /
                    KG_TO_MILKG);
                break;
        }
        if(connection.wormhole.mass_regen)
            text += ' +' + (connection.wormhole.mass_regen / KG_TO_MILKG);
    }
    return text;
}

function ConnectSystems(paper, parentSystem, childSystem) {
    var parentBox = parentSystem.rect.getBBox();
    var childBox = childSystem.rect.getBBox();

    var parentConnRect = paper.rect(
        parentBox.x2 + PARENT_CONNECTION_SQUARE_OFFSET, childBox.y,
        CONNECTION_SQUARE_SIZE, CONNECTION_SQUARE_SIZE);
    var childConnRect = paper.rect(childBox.x - CONNECTION_SQUARE_SIZE -
        CHILD_CONNECTION_SQUARE_OFFSET, childBox.y, CONNECTION_SQUARE_SIZE,
        CONNECTION_SQUARE_SIZE);

    var parentConnRectBox = parentConnRect.getBBox();
    var childConnRectBox = childConnRect.getBBox();
    var triangleTopY = parentConnRectBox.y + (CONNECTION_SQUARE_SIZE / 2) -
                       (CONNECTION_TRIANGLE_WIDTH / 2);
    var triangleMiddleY = parentConnRectBox.y + (CONNECTION_SQUARE_SIZE / 2);
    var triangleBottomY = parentConnRectBox.y + (CONNECTION_SQUARE_SIZE / 2) +
                          (CONNECTION_TRIANGLE_WIDTH / 2);

    var parentConnRectTriangle = paper.path(
        'M' + parentConnRectBox.x2 + ',' + triangleTopY +
        'L' + (parentConnRectBox.x2 + CONNECTION_TRIANGLE_HEIGHT) + ',' +
              triangleMiddleY +
        'L' + parentConnRectBox.x2 + ',' + triangleBottomY +
        'Z');

    var childConnRectTriangle = paper.path(
        'M' + childConnRectBox.x + ',' + triangleTopY +
        'L' + (childConnRectBox.x - CONNECTION_TRIANGLE_HEIGHT) + ',' +
              triangleMiddleY +
        'L' + childConnRectBox.x + ',' + triangleBottomY +
        'Z');

    parentConnRect.triangle = parentConnRectTriangle;
    childConnRect.triangle = childConnRectTriangle;

    parentConnRect.node.classList.add('system-connection');
    childConnRect.node.classList.add('system-connection');
    parentConnRectTriangle.node.classList.add('system-connection');
    childConnRectTriangle.node.classList.add('system-connection');

    var path = paper.path(
        "M" + (parentConnRectBox.x2 + CONNECTION_SQUARE_PATH_OFFSET) + "," +
              triangleMiddleY +
        "L" + (childConnRectBox.x - CONNECTION_SQUARE_PATH_OFFSET) + "," +
              triangleMiddleY);

    path.childNode = childSystem.rect;
    path.childConnRect = childConnRect;
    path.parentConnRect = parentConnRect;
    path.connection = childSystem.parent_connection;
    childSystem.rect.pathToParent = path;
    parentConnRect.path = path;
    childConnRect.path = path;

    if(childSystem.parent_connection) {
        var connection = childSystem.parent_connection;
        var parentConnRectText = GetParentConnRectText(connection);
        var childConnRectText = GetChildConnRectText(connection);

        var connectionLife = GetConnectionLifeText(connection);
        var connectionJumpMass = GetConnectionJumpMassText(connection);
        var connectionMass = GetConnectionMassText(connection);

        var connectionLifeText = paper.text(parentConnRectBox.x2 +
            CONNECTION_SQUARE_TEXT_OFFSET, triangleMiddleY -
            CONNECTION_PATH_TEXT_VERTICAL_OFFSET, connectionLife);

        var connectionJumpMassText = paper.text(childConnRectBox.x -
            CONNECTION_SQUARE_TEXT_OFFSET, triangleMiddleY -
            CONNECTION_PATH_TEXT_VERTICAL_OFFSET, connectionJumpMass);

        var connectionMassText = paper.text(parentConnRectBox.x2 +
            CONNECTION_SQUARE_PATH_OFFSET + (CONNECTION_PATH_LENGTH / 2),
            triangleMiddleY + CONNECTION_PATH_TEXT_VERTICAL_OFFSET,
            connectionMass);

        parentConnRectText = paper.text(parentConnRectBox.x +
            (CONNECTION_SQUARE_SIZE / 2), triangleMiddleY, parentConnRectText);
        childConnRectText = paper.text(childConnRectBox.x +
            (CONNECTION_SQUARE_SIZE / 2), triangleMiddleY, childConnRectText);

        path.connectionLifeText = connectionLifeText;
        path.connectionJumpMassText = connectionJumpMassText;
        path.connectionMassText = connectionMassText;

        path.node.classList.add('wormhole-connection');

        parentConnRect.mouseover(OnConnectionHover);
        childConnRect.mouseover(OnConnectionHover);
        parentConnRect.mouseout(OnConnectionHoverOut);
        childConnRect.mouseout(OnConnectionHoverOut);
        parentConnRect.mousedown(OnConnectionClick);
        childConnRect.mousedown(OnConnectionClick);

        parentConnRectText.mouseover(OnConnectionHover);
        childConnRectText.mouseover(OnConnectionHover);
        parentConnRectText.mouseout(OnConnectionHoverOut);
        childConnRectText.mouseout(OnConnectionHoverOut);
        parentConnRectText.mousedown(OnConnectionClick);
        childConnRectText.mousedown(OnConnectionClick);
    }
    else {
        parentConnRectText = paper.text(parentConnRectBox.x +
            (CONNECTION_SQUARE_SIZE / 2), triangleMiddleY, 'Gate');
        childConnRectText = paper.text(childConnRectBox.x +
            (CONNECTION_SQUARE_SIZE / 2), triangleMiddleY, 'Gate');

        path.node.classList.add('system-connection');
    }

    parentConnRect.text = parentConnRectText;
    childConnRect.text = childConnRectText;
    parentConnRectText.path = path;
    childConnRectText.path = path;
}

function OnSystemHover() {
    var rect;
    if(this.tagName && this.tagName.toLowerCase() == 'div') rect = this.rect;
    else if(this.type == 'rect') rect = this;
    else rect = this.rect;

    var system = rect.system;
    if(!system.$infoPanel && !system.$actionOverlay) {
        if(!system.locked) rect.node.classList.add('hover');

        var rectBox = rect.getBBox();
        system.$infoPanel = $('#stash .system-info').clone().appendTo('#map');
        system.$infoPanel.css({'top': rectBox.y, 'left': rectBox.x2});
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
    var rect;
    if(this.tagName && this.tagName.toLowerCase() == 'div') rect = this.rect;
    else if(this.type == 'rect') rect = this;
    else rect = this.rect;

    var system = rect.system;
    if(system.$infoPanel) {
        rect.node.classList.remove('hover');
        system.$infoPanel.remove();
        system.$infoPanel = null;
    }
}

function OnConnectionHover() {
    var path;
    if(this.tagName && this.tagName.toLowerCase() == 'div')
        path = paper.getById($(this).attr('data-path-id'));
    else path = this.path;

    var connection = path.connection;
    if(!connection.$infoPanel && !connection.$actionOverlay) {
        if(!connection.locked) {
            path.parentConnRect.node.classList.add('hover');
            path.childConnRect.node.classList.add('hover');
        }

        var rectBox = path.childConnRect.getBBox();
        connection.$infoPanel = $('#stash .connection-info').clone().appendTo(
            '#map');
        connection.$infoPanel.css({'top': rectBox.y, 'left': rectBox.x2});
        connection.$infoPanel.children('#connection-info-author').append(
            connection.author);
        connection.$infoPanel.children('#connection-info-date').append(
            connection.date);
        if(connection.locked)
            connection.$infoPanel.children('#connection-info-lock').append(
                connection.locked).removeAttr('hidden');
    }
}

function OnConnectionHoverOut() {
    var path;
    if(this.tagName && this.tagName.toLowerCase() == 'div')
        path = paper.getById($(this).attr('data-path-id'));
    else path = this.path;

    var connection = path.connection;
    if(connection.$infoPanel) {
        path.parentConnRect.node.classList.remove('hover');
        path.childConnRect.node.classList.remove('hover');
        connection.$infoPanel.remove();
        connection.$infoPanel = null;
    }
}

function ClearSelection(softClear) {
    paper.forEach(function(el) {
        if((el.type == 'rect' && el.system && el.system.$actionOverlay) ||
           (el.type == 'path' && el.connection &&
            el.connection.$actionOverlay)) {
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
            if(el.type == 'rect') {
                el.node.classList.remove('hover');
                el.system.$actionOverlay.remove();
                el.system.$actionOverlay = null;
            }
            else {
                el.childConnRect.node.classList.remove('hover');
                el.parentConnRect.node.classList.remove('hover');
                el.connection.$actionOverlay.remove();
                el.connection.$actionOverlay = null;
            }
            return;
        }
    });
}

function ActivateNode(system, rect) {
    if(!system.$actionOverlay) {
        if(system.$infoPanel) {
            system.$infoPanel.remove();
            system.$infoPanel = null;
        }

        var rectBox = rect.getBBox();
        system.$actionOverlay = $('#stash .system-action-overlay').clone()
            .appendTo('#map');
        system.$actionOverlay.css({'top' : rectBox.y, 'left' : rectBox.x,
            'height' : rectBox.height, 'width' : rectBox.width});
        system.$actionOverlay[0].system = system;
    }
}

function OnSystemClick() {
    var rect;
    if(this.type == 'rect') rect = this;
    else rect = this.rect;
    var system = rect.system;

    if(!system.locked && !system.$actionOverlay) {
        if(system.children.length) {
            var checkedDescendants = [];
            var currentNode = system;
            while(currentNode) {
                if(currentNode.children.length &&
                   checkedDescendants.indexOf(currentNode.children[0].id) == -1)
                    currentNode = currentNode.children[0];
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
                ClearSelection(true);
                ActivateNode(system, rect);
            },
            error: function(xhr, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
    }
}

function ActivateConnection(path) {
    if(!path.connection.$actionOverlay) {
        if(path.connection.$infoPanel) {
            path.connection.$infoPanel.remove();
            path.connection.$infoPanel = null;
        }

        var parentConnRectBox = path.parentConnRect.getBBox();
        var childConnRectBox = path.childConnRect.getBBox();
        path.connection.$actionOverlay = $('#stash .connection-action-overlay')
            .clone().appendTo('#map');
        path.connection.$actionOverlay.css({'top' : parentConnRectBox.y,
            'left' : parentConnRectBox.x, 'height' : parentConnRectBox.height,
            'width' : childConnRectBox.x2 - parentConnRectBox.x});
        path.connection.$actionOverlay[0].connection = path.connection;
    }
}

function OnConnectionClick() {
    var path = this.path;
    if(path.connection && !path.connection.locked &&
       !path.connection.$actionOverlay && !path.childNode.system.locked) {
        $.ajax({
            type: 'POST',
            url: '/lock_object/',
            data: {
                'connection_id' : path.connection.id,
                'page_name': window.location.pathname.split('/')[1]
            },
            success: function() {
                ClearSelection(true);
                ActivateConnection(path);
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

function LockOverlayOnNode(rect) {
    var rectBox = rect.getBBox();
    rect.system.$lockOverlay = $('#stash .lock-overlay').clone().appendTo(
        '#map');
    rect.system.$lockOverlay.css({'top' : rectBox.y, 'left' : rectBox.x,
        'height' : rectBox.height, 'width' : rectBox.width});
    rect.system.$lockOverlay[0].rect = rect;
    rect.system.$lockOverlay.on('mouseenter', OnSystemHover);
    rect.system.$lockOverlay.on('mouseleave', OnSystemHoverOut);
}

function LockNode(rect, username, noTraversal) {
    var currentNode = rect.system;
    currentNode.locked = username;
    LockOverlayOnNode(rect);
    if(!noTraversal) {
        if(rect.pathToParent && rect.pathToParent.connection)
            LockConnection(rect.pathToParent, username, true);
        if(currentNode.children.length) {
            while(currentNode) {
                if(currentNode.children.length &&
                   !currentNode.children[0].locked)
                    currentNode = currentNode.children[0];
                else
                    currentNode = TraverseToNextNode(currentNode);
                if(currentNode.id == rect.system.id) break;
                if(!currentNode.locked) {
                    currentNode.locked = username;
                    LockOverlayOnNode(currentNode.rect);
                    if(currentNode.rect.pathToParent &&
                       currentNode.rect.pathToParent.connection)
                        LockConnection(currentNode.rect.pathToParent,
                                       username, true);
                }
            }
        }
    }
}

function UnlockNode(rect, noTraversal) {
    var currentNode = rect.system;
    var locker = currentNode.locked;
    currentNode.locked = null;
    currentNode.$lockOverlay.remove();
    if(rect.pathToParent && rect.pathToParent.connection)
        UnlockConnection(rect.pathToParent, true);
    if(!noTraversal && currentNode.children.length &&
       currentNode.children[0].locked) {
        while(currentNode) {
            if(currentNode.children.length && currentNode.children[0].locked)
                currentNode = currentNode.children[0];
            else
                currentNode = TraverseToNextNode(currentNode);
            if(currentNode.id == rect.system.id) break;
            if(currentNode.locked && currentNode.locked == locker) {
                currentNode.locked = null;
                currentNode.$lockOverlay.remove();
                if(currentNode.rect.pathToParent &&
                   currentNode.rect.pathToParent.connection)
                    UnlockConnection(currentNode.rect.pathToParent, true);
            }
        }
    }
}

function LockConnection(path, username, noTraversal) {
    path.connection.locked = username;

    var parentConnRectBox = path.parentConnRect.getBBox();
    var childConnRectBox = path.childConnRect.getBBox();
    path.connection.$lockOverlay = $('#stash .lock-overlay').clone().appendTo(
        '#map');
    path.connection.$lockOverlay.css({'top' : parentConnRectBox.y,
        'left' : parentConnRectBox.x, 'height' : parentConnRectBox.height,
        'width' : childConnRectBox.x2 - parentConnRectBox.x});
    path.connection.$lockOverlay.attr('data-path-id', path.id);
    path.connection.$lockOverlay.on('mouseenter', OnConnectionHover);
    path.connection.$lockOverlay.on('mouseleave', OnConnectionHoverOut);

    if(!noTraversal) LockNode(path.childNode, username, true);
}

function UnlockConnection(path, noTraversal) {
    path.connection.locked = null;
    path.connection.$lockOverlay.remove();
    if(!noTraversal) UnlockNode(path.childNode, true);
}

function MoveNodeDown(rect, distance) {
    rect.transform('...t0,' + distance);
    rect.text.transform('...t0,' + distance);
    rect.pathToParent.parentConnRect.transform('...t0,' + distance);
    rect.pathToParent.parentConnRect.triangle.transform('...t0,' + distance);
    rect.pathToParent.parentConnRect.text.transform('...t0,' + distance);
    rect.pathToParent.childConnRect.transform('...t0,' + distance);
    rect.pathToParent.childConnRect.triangle.transform('...t0,' + distance);
    rect.pathToParent.childConnRect.text.transform('...t0,' + distance);
    rect.pathToParent.transform('...t0,' + distance);

    if(rect.pathToParent.connection) {
        rect.pathToParent.connectionLifeText.transform('...t0,' + distance);
        rect.pathToParent.connectionJumpMassText.transform('...t0,' + distance);
        rect.pathToParent.connectionMassText.transform('...t0,' + distance);
    }
}


function AddNode(node) {
    paper.forEach(function(elem) {
        if(elem.type == 'rect' && elem.system &&
           elem.system.id == node.parent_node_id) {
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
                    if(el.type == 'rect' && el.system &&
                       el.system.y >= node.y) {
                        el.system.y++;
                        MoveNodeDown(el, RECT_HEIGHT + VERTICAL_LEVEL_OFFSET);
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
            DrawSystem(paper, node);

            return;
        }
    });
}

function MoveNodeUp(rect, distance) {
    rect.transform('...t0,-' + distance);
    rect.text.transform('...t0,-' + distance);
    rect.pathToParent.parentConnRect.transform('...t0,-' + distance);
    rect.pathToParent.parentConnRect.triangle.transform('...t0,-' + distance);
    rect.pathToParent.parentConnRect.text.transform('...t0,-' + distance);
    rect.pathToParent.childConnRect.transform('...t0,-' + distance);
    rect.pathToParent.childConnRect.triangle.transform('...t0,-' + distance);
    rect.pathToParent.childConnRect.text.transform('...t0,-' + distance);
    rect.pathToParent.transform('...t0,-' + distance);

    if(rect.pathToParent.connection) {
        rect.pathToParent.connectionLifeText.transform('...t0,-' + distance);
        rect.pathToParent.connectionJumpMassText.transform(
            '...t0,-' + distance);
        rect.pathToParent.connectionMassText.transform('...t0,-' + distance);
    }
}

function RemoveNodeElements(system) {
    if(system.$infoPanel) system.$infoPanel.remove();
    if(system.$lockOverlay) system.$lockOverlay.remove();

    if(system.rect.pathToParent.connection) {
        if(system.rect.pathToParent.connection.$infoPanel)
            system.rect.pathToParent.connection.$infoPanel.remove();
        if(system.rect.pathToParent.connection.$lockOverlay)
            system.rect.pathToParent.connection.$lockOverlay.remove();

        system.rect.pathToParent.connectionLifeText.remove();
        system.rect.pathToParent.connectionJumpMassText.remove();
        system.rect.pathToParent.connectionMassText.remove();
    }

    system.rect.pathToParent.parentConnRect.triangle.remove();
    system.rect.pathToParent.parentConnRect.text.remove();
    system.rect.pathToParent.parentConnRect.remove();
    system.rect.pathToParent.childConnRect.triangle.remove();
    system.rect.pathToParent.childConnRect.text.remove();
    system.rect.pathToParent.childConnRect.remove();
    system.rect.pathToParent.remove();
    system.rect.text.remove();
    system.rect.remove();
}

function DeleteNode(nodeID) {
    paper.forEach(function(el) {
        if(el.type == 'rect' && el.system && el.system.id == nodeID) {
            var currentNode = el.system;
            var nodeChainWidth = 1;
            while(currentNode) {
                if(currentNode.children.length)
                    currentNode = currentNode.children[0];
                else {
                    if((currentNode.y - el.system.y + 1) > nodeChainWidth)
                        nodeChainWidth = currentNode.y - el.system.y + 1;

                    RemoveNodeElements(currentNode);

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
                                if(elem.type == 'rect' && elem.system &&
                                   elem.system.y > currentNode.y) {
                                    elem.system.y -= nodeChainWidth;
                                    MoveNodeUp(elem, (RECT_HEIGHT +
                                        VERTICAL_LEVEL_OFFSET) *
                                        nodeChainWidth);
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
        if(el.type == 'rect' && el.system) {
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
        if(el.type == 'rect' && el.system && el.system.id == node.id) {
            el.system.author = node.author;
            el.system.date = node.date;
            if(el.system.name != node.name) {
                el.system.name = node.name;
                el.text.attr('text', GetSystemText(node));
                if(el.system.type != node.type) {
                    el.system.type = node.type;
                    ColorSystem(el.system);
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
        if(el.type == 'rect' && el.pathToParent &&
           el.pathToParent.connection &&
           el.pathToParent.connection.id == connection.id) {
            var curConnection = el.pathToParent.connection;
            curConnection.author = connection.author;

            if(curConnection.parent_celestial != connection.parent_celestial ||
               curConnection.wormhole.sig != connection.wormhole.sig) {
                curConnection.parent_celestial = connection.parent_celestial;
                el.pathToParent.parentConnRect.text.attr('text',
                    GetParentConnRectText(connection));
            }

            if(curConnection.child_celestial != connection.child_celestial ||
               curConnection.wormhole.sig != connection.wormhole.sig) {
                curConnection.child_celestial = connection.child_celestial;
                el.pathToParent.childConnRect.text.attr('text',
                    GetChildConnRectText(connection));
            }

            if(curConnection.life_level != connection.life_level ||
               curConnection.wormhole.life != connection.wormhole.life) {
                curConnection.life_level = connection.life_level;
                el.pathToParent.connectionLifeText.attr('text',
                    GetConnectionLifeText(connection));
            }

            if(curConnection.mass_level != connection.mass_level ||
               curConnection.wormhole.total_mass !=
               connection.wormhole.total_mass) {
                curConnection.mass_level = connection.mass_level;
                el.pathToParent.connectionMassText.attr('text',
                    GetConnectionMassText(connection));
            }

            if(curConnection.wormhole.sig != connection.wormhole.sig) {
                if(curConnection.wormhole.jump_mass !=
                   connection.wormhole.jump_mass) {
                    el.pathToParent.connectionJumpMassText.attr('text',
                        GetConnectionJumpMassText(connection));
                }

                curConnection.wormhole = connection.wormhole;

                if(!el.system.name && curConnection.facing_down &&
                   connection.wormhole_type &&
                   el.system.type != connection.wormhole_type) {
                    el.system.type = connection.wormhole_type;
                    el.text.attr('text', GetSystemText(el.system));
                    ColorSystem(el.system);
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
                        if(el.type == 'rect' && el.system && el.system.locked &&
                           el.system.locked == data.object_lock.username) {
                            UnlockNode(el);
                        }
                        else if(el.type == 'path' && el.connection &&
                                el.connection.locked &&
                                el.connection.locked ==
                                data.object_lock.username) {
                            UnlockConnection(el);
                        }
                    });
                }
                paper.forEach(function(el) {
                    if(data.object_lock.type == 'node' &&
                       el.type == 'rect' && el.system &&
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
