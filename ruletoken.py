def genToken(rule):
    dest_zones = rule.findall('to/member')
    d_zone_list = []
    for zone in dest_zones:
        d_zone_list.append((zone.text))
    src_zones = rule.findall('from/member')
    s_zone_list = []
    for zone in src_zones:
        s_zone_list.append(zone.text)
    src_addrs = rule.findall('source/member')
    src_addr_list = []
    for addr in src_addrs:
        src_addr_list.append(addr.text)
    dest_addrs = rule.findall('destination/member')
    dest_addr_list = []
    for addr in dest_addrs:
        dest_addr_list.append(addr.text)
    src_users = rule.findall('source-user/member')
    src_user_list = []
    for user in src_users:
        src_user_list.append(user.text)
    categories = rule.findall('category/member')
    cat_list = []
    for cat in categories:
        cat_list.append(cat.text)
    apps = rule.findall('application/member')
    app_list = []
    for app in apps:
        app_list.append(app.text)
    svcs = rule.findall('service/member')
    svc_list = []
    for svc in svcs:
        svc_list.append(svc.text)
    hips = rule.findall('hip-profiles/member')
    hip_list = []
    for hip in hips:
        hip_list.append(hip.text)
    action = rule.find('action').text
    t_list = d_zone_list + s_zone_list + src_addr_list + dest_addr_list + src_user_list + cat_list + app_list + svc_list + hip_list
    t_list.append(action)
    t_list = "".join(t_list)
    name = rule.attrib['name']
    return (name, t_list)
