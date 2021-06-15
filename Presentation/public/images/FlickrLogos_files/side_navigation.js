var side_navigation = $('.sideNavigation'),
    side_navigation_item_toggles = $('.sideNavigation-itemToggle0'),
    side_navigation_item_selector = '.sideNavigation-item0',
    side_navigation_item2_selector = '.sideNavigation-item1',
    side_navigation_item_open_class = 'sideNavigation-item0--open',
    side_navigation_item2_open_class = 'sideNavigation-item1--open';

/*
    First Level Links
 */
side_navigation_item_toggles.click(function(e) {
    e.preventDefault();

    // toggle class "open" on nav item
    var target_item = $(this).closest(side_navigation_item_selector);
    target_item.toggleClass(side_navigation_item_open_class);

    // max. one nav item can be open at the same time
    target_item.siblings().removeClass(side_navigation_item_open_class);

    // close all inner items
    $(side_navigation_item2_selector).removeClass(side_navigation_item2_open_class);
});
