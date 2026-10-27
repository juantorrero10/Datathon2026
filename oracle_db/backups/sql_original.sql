prompt --application/set_environment
set define off verify off feedback off
whenever sqlerror exit sql.sqlcode rollback
--------------------------------------------------------------------------------
--
-- Oracle APEX export file
--
-- You should run this script using a SQL client connected to the database as
-- the owner (parsing schema) of the application or as a database user with the
-- APEX_ADMINISTRATOR_ROLE role.
--
-- This export file has been automatically generated. Modifying this file is not
-- supported by Oracle and can lead to unexpected application and/or instance
-- behavior now or in the future.
--
-- NOTE: Calls to apex_application_install override the defaults below.
--
--------------------------------------------------------------------------------
begin
wwv_flow_imp.import_begin (
 p_version_yyyy_mm_dd=>'2026.03.30'
,p_release=>'26.1.5'
,p_default_workspace_id=>9407325500210183
,p_default_application_id=>215
,p_default_id_offset=>0
,p_default_owner=>'WKSP_DATATHON'
);
end;
/
 
prompt APPLICATION 215 - Pueblos con Vida
--
-- Application Export:
--   Application:     215
--   Name:            Pueblos con Vida
--   Exported By:     ADMIN
--   Flashback:       0
--   Export Type:     Application Export
--     Pages:                      4
--       Processes:                4
--       Regions:                  4
--     Shared Components:
--       Logic:
--       Navigation:
--         Lists:                  2
--       Security:
--         Authentication:         1
--       User Interface:
--         Themes:                 1
--         Templates:
--       PWA:
--       Globalization:
--       Reports:
--       E-Mail:
--     Supporting Objects:  Included
--   Version:         26.1.5
--   Instance ID:     9389724618832531
--

prompt --application/delete_application
begin
wwv_flow_imp.remove_flow(wwv_flow.g_flow_id);
end;
/
prompt --application/create_application
begin
wwv_imp_workspace.create_flow(
 p_id=>wwv_flow.g_flow_id
,p_owner=>nvl(wwv_flow_application_install.get_schema,'WKSP_DATATHON')
,p_name=>nvl(wwv_flow_application_install.get_application_name,'Pueblos con Vida')
,p_alias=>nvl(wwv_flow_application_install.get_application_alias,'PUEBLOSVIDA215')
,p_page_view_logging=>'YES'
,p_page_protection_enabled_y_n=>'Y'
,p_checksum_salt=>'A1B2C3D4E5F6789012345678901234567890ABCDEF1234567890ABCDEF123456'
,p_bookmark_checksum_function=>'SH512'
,p_max_session_length_sec=>28800
,p_max_session_idle_sec=>3600
,p_compatibility_mode=>'24.2'
,p_flow_language=>'es'
,p_flow_language_derived_from=>'FLOW_PRIMARY_LANGUAGE'
,p_date_format=>'DD/MM/YYYY'
,p_timestamp_format=>'DD/MM/YYYY HH24:MI'
,p_timestamp_tz_format=>'DS'
,p_flow_image_prefix=>nvl(wwv_flow_application_install.get_image_prefix,'')
,p_authentication_id=>wwv_flow_imp.id(8900550584000001)
,p_application_tab_set=>0
,p_logo_type=>'T'
,p_logo_text=>'Pueblos con Vida'
,p_public_user=>'APEX_PUBLIC_USER'
,p_proxy_server=>nvl(wwv_flow_application_install.get_proxy,'')
,p_no_proxy_domains=>nvl(wwv_flow_application_install.get_no_proxy_domains,'')
,p_flow_version=>'24.2.0'
,p_flow_status=>'AVAILABLE_W_EDIT_LINK'
,p_browser_cache=>'N'
,p_browser_frame=>'S'
,p_deep_linking=>'Y'
,p_authorize_batch_job=>'N'
,p_rejoin_existing_sessions=>'N'
,p_csv_encoding=>'Y'
,p_modernization_available=>'Y'
,p_substitution_string_01=>'APP_NAME'
,p_substitution_value_01=>'Pueblos con Vida'
,p_file_prefix=>nvl(wwv_flow_application_install.get_static_app_file_prefix,'')
,p_files_version=>1
,p_version_scn=>'51003540663075'
,p_print_server_type=>'INSTANCE'
,p_file_storage=>'DB'
,p_is_pwa=>'N'
,p_theme_id=>42
,p_home_url=>'f?p=&APP_ID.:1:&APP_SESSION.::&DEBUG.:::'
,p_login_url=>'f?p=&APP_ID.:101:&APP_SESSION.::&DEBUG.:::'
,p_theme_style_by_user_pref=>false
,p_built_with_love=>false
,p_navigation_list_id=>wwv_flow_imp.id(8900550584000004)
,p_navigation_list_position=>'SIDE'
,p_navigation_list_template_id=>2469215554099805162
,p_nav_list_template_options=>'#DEFAULT#:js-defaultCollapsed:js-navCollapsed--hidden:t-TreeNav--styleA'
,p_nav_bar_type=>'LIST'
,p_nav_bar_list_id=>wwv_flow_imp.id(8900550584000005)
,p_nav_bar_list_template_id=>2849019392706229583
,p_nav_bar_template_options=>'#DEFAULT#'
);
end;
/
prompt --application/plugin_settings
begin
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10235482427095855)
,p_plugin_type=>'DYNAMIC ACTION'
,p_plugin=>'NATIVE_OPEN_AI_ASSISTANT'
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10235725621095856)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_COLOR_PICKER'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'display_as', 'POPUP',
  'mode', 'FULL')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10235860659095856)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_DATE_PICKER_APEX'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'appearance_behavior', 'MONTH-PICKER:YEAR-PICKER:TODAY-BUTTON',
  'days_outside_month', 'VISIBLE',
  'show_on', 'FOCUS',
  'time_increment', '15')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10235649897095856)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_GEOCODED_ADDRESS'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'background', 'default',
  'display_as', 'LIST',
  'map_preview', 'POPUP:ITEM',
  'match_mode', 'RELAX_HOUSE_NUMBER')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236190586095857)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_SELECT_MANY'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'display_values_as', 'separated')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10235530645095855)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_SINGLE_CHECKBOX'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'checked_value', 'Y',
  'unchecked_value', 'N')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10235935077095857)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_STAR_RATING'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'default_icon', 'fa-star',
  'tooltip', '#VALUE#')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236091027095857)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_YES_NO'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'display_style', 'SWITCH_CB',
  'off_value', 'N',
  'on_value', 'Y')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236216919095858)
,p_plugin_type=>'PROCESS TYPE'
,p_plugin=>'NATIVE_GEOCODING'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'match_mode', 'RELAX_HOUSE_NUMBER')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236451679095858)
,p_plugin_type=>'REGION TYPE'
,p_plugin=>'NATIVE_DISPLAY_SELECTOR'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'include_slider', 'Y')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236572738095859)
,p_plugin_type=>'REGION TYPE'
,p_plugin=>'NATIVE_IR'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'actions_menu_structure', 'IG')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236336022095858)
,p_plugin_type=>'REGION TYPE'
,p_plugin=>'NATIVE_MAP_REGION'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'use_vector_tile_layers', 'Y')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236628210095859)
,p_plugin_type=>'WEB SOURCE TYPE'
,p_plugin=>'NATIVE_ADFBC'
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236784071095859)
,p_plugin_type=>'WEB SOURCE TYPE'
,p_plugin=>'NATIVE_BOSS'
);
end;
/
prompt --application/shared_components/navigation/lists/navigation_bar
begin
wwv_flow_imp_shared.create_list(
 p_id=>wwv_flow_imp.id(8900550584000005)
,p_name=>'Navigation Bar'
,p_static_id=>'navigation-bar'
,p_version_scn=>'1'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(8900550584000006)
,p_list_item_display_sequence=>10
,p_list_item_link_text=>'&APP_USER.'
,p_static_id=>'app-user'
,p_list_item_link_target=>'#'
,p_list_item_icon=>'fa-user'
,p_list_item_current_type=>'NEVER'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(8900550584000007)
,p_list_item_display_sequence=>20
,p_list_item_link_text=>'Logout'
,p_static_id=>'logout'
,p_list_item_link_target=>'&LOGOUT_URL.'
,p_list_item_icon=>'fa-sign-out'
,p_parent_list_item_id=>wwv_flow_imp.id(8900550584000006)
,p_list_item_current_type=>'NEVER'
);
end;
/
prompt --application/shared_components/navigation/lists/navigation_menu
begin
wwv_flow_imp_shared.create_list(
 p_id=>wwv_flow_imp.id(8900550584000004)
,p_name=>'Navigation Menu'
,p_static_id=>'navigation-menu'
,p_version_scn=>'1'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(8900550584000022)
,p_list_item_display_sequence=>40
,p_list_item_link_text=>'Datos'
,p_static_id=>'datos'
,p_list_item_link_target=>'f?p=&APP_ID.:30:&APP_SESSION.::&DEBUG.:::'
,p_list_item_icon=>'fa-table'
,p_list_item_current_type=>'TARGET_PAGE'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(8900550584000021)
,p_list_item_display_sequence=>30
,p_list_item_link_text=>'Perfil Ciudadano'
,p_static_id=>'perfil-ciudadano'
,p_list_item_link_target=>'f?p=&APP_ID.:20:&APP_SESSION.::&DEBUG.:::'
,p_list_item_icon=>'fa-home'
,p_list_item_current_type=>'TARGET_PAGE'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(8900550584000020)
,p_list_item_display_sequence=>20
,p_list_item_link_text=>'Perfil Institucional'
,p_static_id=>'perfil-institucional'
,p_list_item_link_target=>'f?p=&APP_ID.:10:&APP_SESSION.::&DEBUG.:::'
,p_list_item_icon=>'fa-building'
,p_list_item_current_type=>'TARGET_PAGE'
);
end;
/
prompt --application/shared_components/navigation/listentry
begin
null;
end;
/
prompt --application/shared_components/navigation/navigation_bar
begin
null;
end;
/
prompt --application/shared_components/logic/application_settings
begin
null;
end;
/
prompt --application/shared_components/navigation/tabs/standard
begin
null;
end;
/
prompt --application/shared_components/navigation/tabs/parent
begin
null;
end;
/
prompt --application/pages/page_groups
begin
null;
end;
/
prompt --application/shared_components/navigation/breadcrumbentry
begin
null;
end;
/
prompt --application/shared_components/user_interface/themes
begin
wwv_flow_imp_shared.create_theme(
 p_id=>wwv_flow_imp.id(8900550584000003)
,p_theme_id=>42
,p_static_id=>'universal-theme'
,p_theme_name=>'Universal Theme'
,p_theme_internal_name=>'UNIVERSAL_THEME'
,p_version_identifier=>'26.1'
,p_navigation_type=>'L'
,p_nav_bar_type=>'LIST'
,p_is_locked=>false
,p_current_theme_style_id=>2722798454316704879
,p_default_page_template=>4073832297226169690
,p_default_dialog_template=>2101883943284197310
,p_error_template=>2102634289808461002
,p_printer_friendly_template=>4073832297226169690
,p_login_template=>2102634289808461002
,p_default_button_template=>4073839297780169708
,p_default_region_template=>4073835273271169698
,p_default_chart_template=>4073835273271169698
,p_default_form_template=>4073835273271169698
,p_default_reportr_template=>4073835273271169698
,p_default_wizard_template=>4073835273271169698
,p_default_menur_template=>2532939663579242476
,p_default_listr_template=>4073835273271169698
,p_default_irr_template=>2102002977963900996
,p_default_report_template=>2540130677583398057
,p_default_label_template=>1610598304472262251
,p_default_menu_template=>4073839682315169711
,p_default_list_template=>4073837480889169704
,p_default_top_nav_list_temp=>2528231041045349458
,p_default_side_nav_list_temp=>2469215554099805162
,p_default_nav_list_position=>'SIDE'
,p_default_dialogbtnr_template=>2127905476394690047
,p_default_dialogr_template=>4502917002193490937
,p_default_option_label=>1610598304472262251
,p_default_required_label=>1610598484065263269
,p_default_navbar_list_template=>2849019392706229583
,p_file_prefix=>nvl(wwv_flow_application_install.get_static_theme_file_prefix(42),'#APEX_FILES#themes/theme_42/26.1/')
,p_files_version=>64
,p_icon_library=>'FONTAPEX'
,p_javascript_file_urls=>wwv_flow_string.join(wwv_flow_t_varchar2(
'#APEX_FILES#libraries/apex/#MIN_DIRECTORY#widget.stickyWidget#MIN#.js?v=#APEX_VERSION#',
'#THEME_FILES#js/theme42#MIN#.js?v=#APEX_VERSION#'))
,p_css_file_urls=>'#THEME_FILES#css/Core#MIN#.css?v=#APEX_VERSION#'
,p_reference_id=>wwv_imp_util.get_subscription_id(4073840274158169736,2000,'universal-theme',8842.261)
,p_version_scn_master=>'SH256:WOPVC8vP1TPWUxczh2dJ4mCZcNGSTzA1cn8DjR2oQjY'
);
end;
/
prompt --application/shared_components/user_interface/theme_style
begin
null;
end;
/
prompt --application/shared_components/user_interface/theme_files
begin
null;
end;
/
prompt --application/shared_components/user_interface/template_opt_groups
begin
null;
end;
/
prompt --application/shared_components/user_interface/template_options
begin
null;
end;
/
prompt --application/shared_components/globalization/language
begin
null;
end;
/
prompt --application/shared_components/logic/build_options
begin
null;
end;
/
prompt --application/shared_components/globalization/messages
begin
null;
end;
/
prompt --application/shared_components/globalization/dyntranslations
begin
null;
end;
/
prompt --application/shared_components/security/authentications/app_authentication
begin
wwv_flow_imp_shared.create_authentication(
 p_id=>wwv_flow_imp.id(8900550584000001)
,p_name=>'App Authentication'
,p_static_id=>'app-authentication'
,p_scheme_type=>'NATIVE_APEX_ACCOUNTS'
,p_invalid_session_type=>'LOGIN'
,p_use_secure_cookie_yn=>'N'
,p_ras_mode=>0
,p_version_scn=>'1'
);
end;
/
prompt --application/user_interfaces/combined_files
begin
null;
end;
/
prompt --application/pages/page_00001
begin
wwv_flow_imp_page.create_page(
 p_id=>1
,p_name=>'Inicio'
,p_alias=>'INICIO'
,p_step_title=>'Inicio'
,p_autocomplete_on_off=>'OFF'
,p_step_template=>4073832297226169690
,p_page_template_options=>'#DEFAULT#'
,p_page_is_public_y_n=>'Y'
,p_protection_level=>'C'
,p_page_component_map=>'13'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(8900550584000009)
,p_plug_name=>'Portada'
,p_static_id=>'portada'
,p_region_template_options=>'#DEFAULT#'
,p_plug_template=>4073835273271169698
,p_plug_display_sequence=>10
,p_plug_item_display_point=>'ABOVE'
,p_location=>null
,p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(
'BEGIN HTP.P(q''~<style>',
'.pvh{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;max-width:1100px;margin:0 auto;color:#0f172a}',
'.pvh .hero{background:linear-gradient(135deg,#0f2a44,#163a5c);color:#fff;border-radius:18px;padding:34px 34px 30px;margin:8px 0 20px}',
'.pvh .kick{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#9fd8d0;font-weight:800}',
'.pvh h1{font-size:36px;line-height:1.1;margin:8px 0 8px;letter-spacing:-.02em}',
'.pvh .sub{color:#cfe0ee;font-size:15px;max-width:760px;line-height:1.5;margin:0}',
'.pvh .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}',
'.pvh .card{display:block;text-decoration:none;color:inherit;background:#fff;border:1px solid #dbe3ea;border-radius:16px;padding:22px;box-shadow:0 1px 2px rgba(15,42,68,.05),0 8px 22px rgba(15,42,68,.07);transition:transform .15s,box-shadow .15s}',
'.pvh .card:hover{transform:translateY(-2px);box-shadow:0 12px 30px rgba(15,42,68,.12)}',
'.pvh .ico{width:42px;height:42px;border-radius:12px;background:#eefaf8;color:#0f766e;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;margin-bottom:12px}',
'.pvh h2{font-size:19px;margin:0 0 6px;color:#0f2a44}',
'.pvh p{font-size:13px;color:#5b6b7c;line-height:1.5;margin:0 0 10px}',
'.pvh .go{font-size:12px;font-weight:800;color:#0f766e}',
'.pvh .foot{font-size:11px;color:#64748b;margin:16px 0 4px;line-height:1.5}',
'@media(max-width:800px){.pvh .cards{grid-template-columns:1fr}.pvh h1{font-size:28px}.pvh .hero{padding:24px}}',
'</style>',
'<div class="pvh">',
'  <div class="hero">',
unistr('    <div class="kick">II Datathon LoDCOREMadrid \00B7 2026</div>'),
'    <h1>Pueblos con Vida</h1>',
unistr('    <p class="sub">155 municipios de menos de 50.000 habitantes, datos abiertos 2010-2025, proyecci\00F3n a 2035 y un simulador para decidir d\00F3nde puede crecer la Comunidad de Madrid.</p>'),
'  </div>',
'  <div class="cards">',
'    <a class="card" href="#" data-page="10">',
unistr('      <div class="ico">\D83C\DFDB</div><h2>Perfil institucional</h2>'),
unistr('      <p>Simula nuevos residentes, vivienda, sanidad, escuelas y transporte. Ve el efecto en el \00EDndice, en los ratios por habitante, en los vecinos y en la proyecci\00F3n 2035.</p>'),
unistr('      <div class="go">Abrir simulador \2192</div>'),
'    </a>',
'    <a class="card" href="#" data-page="20">',
unistr('      <div class="ico">\D83C\DFE1</div><h2>Perfil ciudadano</h2>'),
unistr('      <p>Elige tiempo a Madrid, precio, servicios y empleo. Obt\00E9n un ranking explicado, mapa de afinidad y ficha con la poblaci\00F3n proyectada a 2035.</p>'),
unistr('      <div class="go">Buscar mi municipio \2192</div>'),
'    </a>',
'    <a class="card" href="#" data-page="30">',
unistr('      <div class="ico">\D83D\DCCA</div><h2>Datos abiertos</h2>'),
unistr('      <p>Consulta las tablas completas de los 155 municipios: indicadores, proyecci\00F3n 2035, banda de incertidumbre y presi\00F3n sobre servicios. Descarga en CSV.</p>'),
unistr('      <div class="go">Ver las tablas \2192</div>'),
'    </a>',
'  </div>',
unistr('  <div class="foot">Fuentes: Comunidad de Madrid, INE, IGN y CRTM. Precios de escritura: Notariado v\00EDa S\00F3kerim (CC-BY 4.0). Licencia de salida CC-BY. Atribuci\00F3n CRTM: Powered by CRTM. Los huecos son NA: no se imputan.</div>'),
'</div>',
'<script>',
'document.querySelectorAll(''[data-page]'').forEach(function(a){a.addEventListener(''click'',function(e){e.preventDefault();location.href=''f?p=''+apex.env.APP_ID+'':''+a.getAttribute(''data-page'')+'':''+apex.env.APP_SESSION;});});',
'</script>~''); END;'))
,p_plug_source_type=>'NATIVE_PLSQL'
);
end;
/
prompt --application/pages/page_00010
begin
wwv_flow_imp_page.create_page(
 p_id=>10
,p_name=>'Perfil Institucional'
,p_alias=>'PERFIL-INSTITUCIONAL'
,p_step_title=>'Perfil Institucional'
,p_autocomplete_on_off=>'OFF'
,p_step_template=>4073832297226169690
,p_page_template_options=>'#DEFAULT#'
,p_page_is_public_y_n=>'Y'
,p_protection_level=>'C'
,p_page_component_map=>'10'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(8900550584000013)
,p_plug_name=>'Dashboard institucional'
,p_static_id=>'dashboard-institucional'
,p_region_template_options=>'#DEFAULT#'
,p_plug_template=>4073835273271169698
,p_plug_display_sequence=>10
,p_plug_item_display_point=>'ABOVE'
,p_location=>null
,p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(
'BEGIN HTP.P(q''~<style>',
'.pv10{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#0f172a;max-width:1400px;margin:0 auto}',
'.pv10 .head{display:flex;justify-content:space-between;gap:16px;align-items:flex-end;flex-wrap:wrap;margin:4px 0 16px}',
'.pv10 .kick{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#0f766e;font-weight:800}',
'.pv10 h1{font-size:28px;line-height:1.15;margin:4px 0 4px;color:#0f2a44;letter-spacing:-.02em}',
'.pv10 .sub{font-size:13px;color:#5b6b7c;margin:0;max-width:760px}',
'.pv10 .tag{font-size:11px;background:#eefaf8;border:1px solid #cdeee8;color:#0f766e;border-radius:99px;padding:6px 10px;font-weight:700;white-space:nowrap}',
'.pv10 .grid{display:grid;grid-template-columns:290px minmax(0,1fr);gap:16px;align-items:start}',
'.pv10 .card{background:#fff;border:1px solid #dbe3ea;border-radius:14px;padding:15px;box-shadow:0 1px 2px rgba(15,42,68,.05),0 8px 22px rgba(15,42,68,.06)}',
'.pv10 .panel{position:sticky;top:12px}',
'.pv10 .panel h2{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:#5b6b7c;margin:0 0 12px}',
'.pv10 label{display:block;font-size:12px;font-weight:700;color:#334155;margin:10px 0 4px}',
'.pv10 input,.pv10 select{width:100%;padding:8px 9px;border:1px solid #cbd5e1;border-radius:8px;font:inherit;background:#fff;color:#0f172a}',
'.pv10 input[type=number]{font-variant-numeric:tabular-nums}',
'.pv10 .btn{width:100%;margin-top:14px;background:#0f766e;color:#fff;border:0;border-radius:9px;padding:11px 12px;font-weight:800;cursor:pointer}',
'.pv10 .btn:hover{filter:brightness(1.06)}',
'.pv10 .note{font-size:11px;color:#5b6b7c;line-height:1.45;margin-top:12px;background:#f4f7fa;border:1px solid #e2e8f0;border-radius:9px;padding:9px}',
'.pv10 .kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:14px}',
'.pv10 .kpi{background:#fff;border:1px solid #dbe3ea;border-radius:12px;padding:12px 14px;box-shadow:0 1px 2px rgba(15,42,68,.04)}',
'.pv10 .kpi .l{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#5b6b7c;font-weight:800}',
'.pv10 .kpi b{display:block;font-size:25px;color:#0f2a44;margin-top:3px;letter-spacing:-.02em}',
'.pv10 .kpi .s{font-size:11px;color:#5b6b7c}',
'.pv10 .row{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}',
'.pv10 h3{font-size:14px;margin:0 0 10px;color:#0f2a44}',
'.pv10 .dim{display:grid;grid-template-columns:100px 1fr 1fr 86px;gap:7px;align-items:center;font-size:11px;margin:8px 0}',
'.pv10 .dim span{font-weight:700;color:#334155}',
'.pv10 .track{height:8px;background:#eef2f6;border-radius:99px;overflow:hidden}',
'.pv10 .track i{display:block;height:100%;border-radius:99px}',
'.pv10 .track .before{background:#cbd5e1}',
'.pv10 .track .after{background:#14b8a6}',
'.pv10 .dim b{text-align:right;font-variant-numeric:tabular-nums;color:#0f2a44}',
'.pv10 .legend{font-size:10px;color:#64748b;display:flex;gap:12px;margin:4px 0 6px}',
'.pv10 .legend i{display:inline-block;width:14px;height:7px;border-radius:2px;margin-right:3px}',
'.pv10 .svg{display:block;width:100%;height:auto;background:#fbfdff;border:1px solid #eef3f7;border-radius:9px}',
'.pv10 .spark{display:block;width:100%;height:auto}',
'.pv10 table{width:100%;border-collapse:collapse;font-size:11.5px}',
'.pv10 th{text-align:left;color:#5b6b7c;font-size:10px;text-transform:uppercase;letter-spacing:.05em;background:#f6f9fb;padding:7px 6px;border-bottom:1px solid #dbe3ea}',
'.pv10 td{padding:6px;border-bottom:1px solid #eef2f6}',
'.pv10 .num{text-align:right;font-variant-numeric:tabular-nums}',
'.pv10 .warn{display:block;margin-top:8px;font-size:11px;color:#92400e;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:8px}',
'.pv10 .up{color:#0f766e}.pv10 .down{color:#b91c1c}',
'.pv10 .seg{display:inline-flex;border:1px solid #cbd5e1;border-radius:8px;overflow:hidden}',
'.pv10 .seg button{border:0;background:#fff;padding:5px 9px;font:inherit;font-size:11px;font-weight:700;color:#475569;cursor:pointer}',
'.pv10 .seg button.on{background:#0f766e;color:#fff}',
'.pv10 .p35{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}',
'.pv10 .p35>div{border-left:3px solid #14b8a6;padding-left:10px}',
'.pv10 .p35 span{display:block;font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:#5b6b7c;font-weight:800}',
'.pv10 .p35 b{display:block;font-size:20px;color:#0f2a44;margin-top:2px}',
'.pv10 .p35 small{font-size:10.5px;color:#64748b}',
'@media(max-width:980px){.pv10 .grid,.pv10 .row{grid-template-columns:1fr}.pv10 .kpis{grid-template-columns:repeat(2,1fr)}.pv10 .panel{position:static}.pv10 .p35{grid-template-columns:repeat(2,1fr)}}',
'</style>',
'<div class="pv10">',
'  <div class="head">',
unistr('    <div><div class="kick">Perfil institucional</div><h1>Simulador de acogida</h1><p class="sub">Elige un municipio y simula el efecto de nuevos residentes, vivienda y equipamientos. El \00EDndice se recalcula con los 155 municipios reales y la ficha inc')
||unistr('luye la proyecci\00F3n a 2035.</p></div>'),
unistr('    <div class="tag">Datos reales \00B7 155 municipios \00B7 proyecci\00F3n 2035</div>'),
'  </div>',
'  <div class="grid">',
'    <aside class="card panel">',
'      <h2>Escenario</h2>',
'      <label>Municipio</label><select id="f10-mun"></select>',
'      <label>Nuevos residentes</label><input id="f10-pop" type="number" value="2000" min="0" step="100">',
'      <label>Nuevas viviendas</label><input id="f10-viv" type="number" value="500" min="0" step="50">',
'      <label>Nuevos centros de salud</label><input id="f10-salud" type="number" value="1" min="0" step="1">',
'      <label>Nuevos centros educativos</label><input id="f10-esc" type="number" value="1" min="0" step="1">',
'      <label>Nuevas paradas de transporte</label><input id="f10-paradas" type="number" value="10" min="0" step="1">',
'      <button class="btn" id="f10-run" type="button">Simular escenario</button>',
unistr('      <div class="note">El modelo usa percentiles de los 155 municipios. No es una predicci\00F3n causal: es un escenario condicional. Los municipios sin dato de tiempo o precio no se inventan.</div>'),
'    </aside>',
'    <section>',
'      <div class="kpis">',
unistr('        <div class="kpi"><div class="l">\00CDndice antes</div><b id="k10-before">\2014</b><div class="s">0-100</div></div>'),
unistr('        <div class="kpi"><div class="l">\00CDndice despu\00E9s</div><b id="k10-after">\2014</b><div class="s">0-100</div></div>'),
unistr('        <div class="kpi"><div class="l">Variaci\00F3n</div><b id="k10-delta">\2014</b><div class="s">puntos</div></div>'),
unistr('        <div class="kpi"><div class="l">Poblaci\00F3n despu\00E9s</div><b id="k10-pob">\2014</b><div class="s">habitantes</div></div>'),
'      </div>',
'      <div class="row">',
unistr('        <div class="card"><h3>Dimensiones: antes vs. despu\00E9s</h3><div class="legend"><span><i style="background:#cbd5e1"></i>antes</span><span><i style="background:#14b8a6"></i>despu\00E9s</span></div><div id="f10-dims"></div></div>'),
unistr('        <div class="card"><h3>Poblaci\00F3n 2010-2035</h3><div class="legend"><span><i style="background:#0f766e"></i>observada (padr\00F3n)</span><span><i style="background:#94a3b8"></i>proyecci\00F3n</span></div><div id="f10-spark"></div></div>'),
'      </div>',
unistr('      <div class="card" style="margin-top:14px"><h3>Proyecci\00F3n 2035</h3><div class="p35">'),
unistr('        <div><span>Poblaci\00F3n 2035</span><b id="p10-p35">\2014</b><small id="p10-band">banda 80 %: \2014</small></div>'),
unistr('        <div><span>Variaci\00F3n 2025-2035</span><b id="p10-crec">\2014</b><small id="p10-abs">\2014</small></div>'),
unistr('        <div><span>Tendencia anual</span><b id="p10-tasa">\2014</b><small id="p10-esc">\2014</small></div>'),
unistr('        <div><span>Fiabilidad</span><b id="p10-fiab">\2014</b><small id="p10-metodo">modelo tendencial anclado</small></div>'),
'      </div></div>',
'      <div class="row">',
unistr('        <div class="card"><h3>Mapa de oportunidad</h3><div class="seg" id="f10-seg"><button type="button" data-mode="indice" class="on">\00CDndice 2025</button><button type="button" data-mode="crec">Crecimiento 2035</button></div><div class="legend" id="')
||'f10-legend"></div><div id="f10-map"></div></div>',
'        <div class="card"><h3>Municipios vecinos</h3><div id="f10-vecinos"></div></div>',
'      </div>',
'      <div class="card" style="margin-top:14px"><h3>Lectura del escenario</h3><div id="f10-text" style="font-size:13px;color:#334155;line-height:1.6"></div></div>',
'    </section>',
'  </div>',
'</div>',
'<script>',
'(function(){',
'  var DATA=[];',
'  function $(id){return document.getElementById(id);}',
unistr('  function fmt(v,d){if(v===null||v===undefined||isNaN(v))return ''\2014'';return Number(v).toLocaleString(''es-ES'',{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}'),
'  function esc(s){return String(s).replace(/[&<>"'']/g,function(c){return {''&'':''&amp;'',''<'':''&lt;'',''>'':''&gt;'',''"'':''&quot;'',"''":''&#39;''}[c];});}',
'  function api(name,params,cb){apex.server.process(name,params,{success:function(d){try{cb(typeof d===''string''?JSON.parse(d):d);}catch(e){console.error(e);}},error:function(x){if(!window.__pvTries)window.__pvTries=0;if(window.__pvTries++<8){setTimeou'
||'t(function(){api(name,params,cb);},900);}else{console.error(x);}}});}',
'  function spark(series,proy){var hist=(series||[]).map(Number);if(!hist.length)return '''';var pr=(proy||[]).map(Number);var all=hist.concat(pr),n=all.length,W=420,H=130,P=16;var mn=Math.min.apply(null,all),mx=Math.max.apply(null,all);function X(i){re'
||'turn P+i/(n-1)*(W-2*P);}function Y(v){return H-P-(v-mn)/((mx-mn)||1)*(H-2*P);}var dh=hist.map(function(v,i){return (i?''L'':''M'')+X(i).toFixed(1)+'',''+Y(v).toFixed(1);}).join('' '');var dp=pr.map(function(v,i){return ''L''+X(hist.length+i).toFixed(1)+'',''+Y(v'
||').toFixed(1);}).join('' '');var x25=X(hist.length-1);var area=dh+'' L''+x25.toFixed(1)+'',''+(H-P)+'' L''+P+'',''+(H-P)+'' Z'';var out=''<svg viewBox="0 0 ''+W+'' ''+H+''" class="spark">'';out+=''<path d="''+area+''" fill="rgba(20,184,166,.10)"></path>'';out+=''<path d="''+'
||'dh+''" fill="none" stroke="#0f766e" stroke-width="2"></path>'';if(pr.length){out+=''<path d="M''+x25.toFixed(1)+'',''+Y(hist[hist.length-1]).toFixed(1)+'' ''+dp+''" fill="none" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4 3"></path>'';}out+=''<line x1='
||'"''+x25.toFixed(1)+''" y1="''+P+''" x2="''+x25.toFixed(1)+''" y2="''+(H-P)+''" stroke="#e2e8f0" stroke-width="1"></line>'';out+=''<text x="''+P+''" y="''+(H-2)+''" font-size="9" fill="#64748b">2010</text><text x="''+x25.toFixed(1)+''" y="''+(H-2)+''" font-size="9" fil'
||'l="#64748b" text-anchor="middle">2025</text>'';if(pr.length){out+=''<text x="''+(W-P)+''" y="''+(H-2)+''" font-size="9" fill="#64748b" text-anchor="end">2035</text>'';}out+=''</svg>'';return out;}',
'  var MAPMODE=''indice'';',
unistr('  function legend(){if(MAPMODE===''crec'')return ''<span><i style="background:#0f766e"></i>25 % o m\00E1s</span><span><i style="background:#14b8a6"></i>15-25 %</span><span><i style="background:#5eead4"></i>8-15 %</span><span><i style="background:#bae6fd"></')
||'i>&lt;8 %</span>'';return ''<span><i style="background:#0f766e"></i>65+</span><span><i style="background:#14b8a6"></i>50-65</span><span><i style="background:#5eead4"></i>35-50</span><span><i style="background:#bae6fd"></i>&lt;35</span>'';}',
'  function drawMap(selected){var pts=DATA.filter(function(m){return m.lat!=null&&m.lon!=null;});if(!pts.length){$(''f10-map'').innerHTML=''<p>Sin datos de coordenadas.</p>'';return;}var mnLon=Math.min.apply(null,pts.map(function(m){return m.lon;})),mxLon'
||'=Math.max.apply(null,pts.map(function(m){return m.lon;})),mnLat=Math.min.apply(null,pts.map(function(m){return m.lat;})),mxLat=Math.max.apply(null,pts.map(function(m){return m.lat;}));var W=640,H=420,P=20,s=Math.min((W-2*P)/((mxLon-mnLon)||1),(H-2*P)'
||'/((mxLat-mnLat)||1)),ox=(W-(mxLon-mnLon)*s)/2,oy=(H-(mxLat-mnLat)*s)/2,out=[''<svg viewBox="0 0 ''+W+'' ''+H+''" class="svg">''];pts.forEach(function(m){var x=ox+(m.lon-mnLon)*s,y=oy+(mxLat-m.lat)*s,r=3.5+(m.pob||0)/40000*5,c,ttl;if(MAPMODE===''crec''){c=m.c'
||unistr('rec>=25?''#0f766e'':m.crec>=15?''#14b8a6'':m.crec>=8?''#5eead4'':''#bae6fd'';ttl=esc(m.nombre)+'' \00B7 crecimiento ''+fmt(m.crec,1)+'' % \00B7 ''+fmt(m.pob)+'' \2192 ''+fmt(m.p2035)+'' hab.'';}else{c=m.indice>=65?''#0f766e'':m.indice>=50?''#14b8a6'':m.indice>=35?''#5eead4'':''#bae6fd')
||unistr(''';ttl=esc(m.nombre)+'' \00B7 \00EDndice ''+fmt(m.indice,1)+'' \00B7 ''+fmt(m.pob)+'' hab.'';}var st=m.cod===selected?''#0f172a'':''#ffffff'',sw=m.cod===selected?2.5:1;out.push(''<circle cx="''+x.toFixed(1)+''" cy="''+y.toFixed(1)+''" r="''+r.toFixed(1)+''" fill="''+c+''" stroke="''')
||'+st+''" stroke-width="''+sw+''"><title>''+ttl+''</title></circle>'');});out.push(''</svg>'');$(''f10-map'').innerHTML=out.join('''');}',
'  function run(){var cod=$(''f10-mun'').value;if(!cod)return;api(''SIMULAR'',{x01:cod,x02:$(''f10-pop'').value||0,x03:$(''f10-viv'').value||0,x04:$(''f10-salud'').value||0,x05:$(''f10-esc'').value||0,x06:$(''f10-paradas'').value||0},render);}',
'  function render(r){$(''k10-before'').textContent=fmt(r.indice_antes,1);$(''k10-after'').textContent=fmt(r.indice_despues,1);$(''k10-delta'').textContent=(r.delta_indice>0?''+'':'''')+fmt(r.delta_indice,1);$(''k10-delta'').className=r.delta_indice>0?''up'':(r.del'
||'ta_indice<0?''down'':'''');$(''k10-pob'').textContent=fmt(r.poblacion_despues,0);',
unistr('    var dims=[[''Demograf\00EDa'',''dem''],[''Vivienda'',''viv''],[''Servicios'',''ser''],[''Accesibilidad'',''acc''],[''Empleo'',''emp'']];'),
'    $(''f10-dims'').innerHTML=dims.map(function(d){var a=r[''dim_''+d[1]+''_antes''],b=r[''dim_''+d[1]+''_despues''];return ''<div class="dim"><span>''+d[0]+''</span><div class="track"><i class="before" style="width:''+(a||0)+''%"></i></div><div class="track"><i cl'
||unistr('ass="after" style="width:''+(b||0)+''%"></i></div><b>''+fmt(a,0)+'' \2192 ''+fmt(b,0)+''</b></div>'';}).join('''');'),
'    var m=DATA.filter(function(x){return x.cod===r.cod;})[0]||{};',
'    $(''f10-spark'').innerHTML=spark(m.serie||[],m.proy||[]);',
'    $(''p10-p35'').textContent=fmt(m.p2035,0);',
unistr('    $(''p10-band'').textContent=''banda 80 %: ''+fmt(m.p10,0)+'' \2013 ''+fmt(m.p90,0);'),
'    $(''p10-crec'').textContent=(m.crec>0?''+'':'''')+fmt(m.crec,1)+'' %'';',
'    $(''p10-abs'').textContent=(m.p2035-m.pob>0?''+'':'''')+fmt(m.p2035-m.pob,0)+'' habitantes'';',
unistr('    $(''p10-tasa'').textContent=(m.tasa>0?''+'':'''')+fmt(m.tasa,2)+'' %/a\00F1o'';'),
unistr('    $(''p10-esc'').textContent=m.esc||''\2014'';'),
unistr('    $(''p10-fiab'').textContent=m.fiabp||''\2014'';'),
'    drawMap(r.cod);',
'    var v=m.vecinos||[];',
unistr('    $(''f10-vecinos'').innerHTML=''<table><thead><tr><th>Vecino</th><th class="num">Dist.</th><th class="num">\00CDndice</th><th>Factor</th></tr></thead><tbody>''+v.map(function(x){return ''<tr><td>''+esc(x.nombre)+''</td><td class="num">''+fmt(x.dist,1)+'' km</t')
||unistr('d><td class="num">''+fmt(x.indice,1)+''</td><td>''+esc(x.factor||''\2014'')+''</td></tr>'';}).join('''')+''</tbody></table>'';'),
'    var t=''El factor limitante del escenario es <b>''+esc(r.factor_limitante)+''</b>. '';',
unistr('    t+=''Sanidad: ''+fmt(r.salud_10k_antes,2)+'' \2192 ''+fmt(r.salud_10k_despues,2)+'' centros por 10.000 hab. '';'),
unistr('    t+=''Escuelas: ''+fmt(r.escuelas_1000_antes,2)+'' \2192 ''+fmt(r.escuelas_1000_despues,2)+'' por 1.000 hab. '';'),
unistr('    t+=''Paradas: ''+fmt(r.paradas_1000_antes,2)+'' \2192 ''+fmt(r.paradas_1000_despues,2)+'' por 1.000 hab. '';'),
unistr('    t+=''Vivienda: ''+fmt(r.viv_1000_antes,0)+'' \2192 ''+fmt(r.viv_1000_despues,0)+'' por 1.000 hab. '';'),
unistr('    if(m.p2035){t+=''<br><br>En 2035 el municipio tendr\00EDa <b>''+fmt(m.p2035,0)+'' habitantes</b> (banda 80 %: ''+fmt(m.p10,0)+'' \2013 ''+fmt(m.p90,0)+''), un ''+fmt(m.crec,1)+'' % m\00E1s, en escenario \00AB''+esc(m.esc)+''\00BB y fiabilidad ''+esc(m.fiabp)+''. Si no se ampl\00EDa ')
||unistr('la oferta, la presi\00F3n pasar\00EDa de ''+fmt(m.san25,0)+'' a ''+fmt(m.san35,0)+'' habitantes por equipamiento sanitario y de ''+fmt(m.viv25,2)+'' a ''+fmt(m.viv35,2)+'' por vivienda.'';}'),
unistr('    t+=''<span class="warn">Los vecinos se muestran como contexto territorial; no se modela un efecto causal de spillover. El \00EDndice usa la misma escala de percentiles que el dataset. La proyecci\00F3n 2035 es tendencial, anclada al crecimiento oficial de')
||unistr(' la CAM: no es una predicci\00F3n causal.</span>'';'),
'    $(''f10-text'').innerHTML=t;',
'  }',
'  function pvBoot(){',
'    var sel=$(''f10-mun'');',
'    sel.addEventListener(''change'',run);',
'    $(''f10-run'').addEventListener(''click'',run);',
'    $(''f10-legend'').innerHTML=legend();',
'    document.querySelectorAll(''#f10-seg button'').forEach(function(b){b.addEventListener(''click'',function(){MAPMODE=b.getAttribute(''data-mode'');document.querySelectorAll(''#f10-seg button'').forEach(function(x){x.classList.toggle(''on'',x===b);});$(''f10-l'
||'egend'').innerHTML=legend();drawMap(sel.value);});});',
'    api(''DATOS'',{},function(rows){DATA=rows;sel.innerHTML=DATA.map(function(m){return ''<option value="''+m.cod+''">''+esc(m.nombre)+''</option>'';}).join('''');sel.value=''28130'';drawMap(''28130'');run();});',
'  }',
'(function pvWait(){ if(window.apex && window.apex.server){ setTimeout(pvBoot,1200); } else { setTimeout(pvWait,100); } })();',
'})();',
'</script>~''); END;'))
,p_plug_source_type=>'NATIVE_PLSQL'
);
wwv_flow_imp_page.create_page_process(
 p_id=>wwv_flow_imp.id(8900550584000011)
,p_process_sequence=>10
,p_process_point=>'ON_DEMAND'
,p_process_type=>'NATIVE_PLSQL'
,p_process_name=>'DATOS'
,p_static_id=>'datos'
,p_process_sql_clob=>wwv_flow_string.join(wwv_flow_t_varchar2(
'DECLARE',
'  v_json CLOB; v_len PLS_INTEGER; v_pos PLS_INTEGER := 1;',
'BEGIN',
'  APEX_JSON.INITIALIZE_CLOB_OUTPUT; APEX_JSON.OPEN_ARRAY;',
'  FOR m IN (SELECT * FROM WKSP_DATATHON.PV_MUN_2035 ORDER BY nombre) LOOP',
'    APEX_JSON.OPEN_OBJECT;',
'    APEX_JSON.WRITE(''cod'', m.cod_ine); APEX_JSON.WRITE(''nombre'', m.nombre); APEX_JSON.WRITE(''pob'', m.poblacion);',
'    APEX_JSON.WRITE(''lat'', m.lat); APEX_JSON.WRITE(''lon'', m.lon); APEX_JSON.WRITE(''dist'', m.distancia_sol_km);',
'    APEX_JSON.WRITE(''tiempo'', m.tiempo_centro_min); APEX_JSON.WRITE(''modo'', m.modo); APEX_JSON.WRITE(''paradas'', m.paradas_total);',
'    APEX_JSON.WRITE(''escuelas'', m.escuelas); APEX_JSON.WRITE(''precio'', m.precio_medio); APEX_JSON.WRITE(''precio_m2'', m.precio_m2);',
'    APEX_JSON.WRITE(''compraventas'', m.compraventas); APEX_JSON.WRITE(''fiabilidad'', m.fiabilidad);',
'    APEX_JSON.WRITE(''dem'', m.dim_dem); APEX_JSON.WRITE(''viv'', m.dim_viv); APEX_JSON.WRITE(''ser'', m.dim_ser);',
'    APEX_JSON.WRITE(''acc'', m.dim_acc); APEX_JSON.WRITE(''emp'', m.dim_emp); APEX_JSON.WRITE(''indice'', m.indice);',
'    APEX_JSON.WRITE(''factor'', m.factor_limitante);',
'    APEX_JSON.WRITE(''p2035'', m.poblacion_2035); APEX_JSON.WRITE(''p10'', m.pob_2035_p10); APEX_JSON.WRITE(''p90'', m.pob_2035_p90);',
'    APEX_JSON.WRITE(''crec'', m.crecimiento_pct); APEX_JSON.WRITE(''esc'', m.escenario); APEX_JSON.WRITE(''fiabp'', m.fiab_pronostico);',
'    APEX_JSON.WRITE(''tasa'', m.tasa_2035_pct); APEX_JSON.WRITE(''conv'', m.pob_2035_convergencia); APEX_JSON.WRITE(''pers'', m.pob_2035_persistencia);',
'    APEX_JSON.WRITE(''san25'', m.hab_sanit_2025); APEX_JSON.WRITE(''san35'', m.hab_sanit_2035);',
'    APEX_JSON.WRITE(''edu25'', m.hab_escuela_2025); APEX_JSON.WRITE(''edu35'', m.hab_escuela_2035);',
'    APEX_JSON.WRITE(''par25'', m.hab_parada_2025); APEX_JSON.WRITE(''par35'', m.hab_parada_2035);',
'    APEX_JSON.WRITE(''viv25'', m.hab_vivienda_2025); APEX_JSON.WRITE(''viv35'', m.hab_vivienda_2035);',
'    APEX_JSON.OPEN_ARRAY(''serie'');',
'    FOR s IN (SELECT poblacion FROM WKSP_DATATHON.PV_SERIE WHERE cod_ine=m.cod_ine ORDER BY anio) LOOP APEX_JSON.WRITE(s.poblacion); END LOOP;',
'    APEX_JSON.CLOSE_ARRAY;',
'    APEX_JSON.OPEN_ARRAY(''proy'');',
'    FOR s IN (SELECT poblacion FROM WKSP_DATATHON.PV_PROYECCION_SERIE WHERE cod_ine=m.cod_ine ORDER BY anio) LOOP APEX_JSON.WRITE(s.poblacion); END LOOP;',
'    APEX_JSON.CLOSE_ARRAY;',
'    APEX_JSON.OPEN_ARRAY(''vecinos'');',
'    FOR v IN (SELECT v.nombre_vecino, v.distancia_km, b.indice, b.factor_limitante, b.tiempo_centro_min',
'              FROM WKSP_DATATHON.PV_VECINOS v JOIN WKSP_DATATHON.PV_MUN_BASE b ON b.cod_ine=v.cod_vecino',
'              WHERE v.cod_ine=m.cod_ine ORDER BY v.distancia_km) LOOP',
'      APEX_JSON.OPEN_OBJECT; APEX_JSON.WRITE(''nombre'', v.nombre_vecino); APEX_JSON.WRITE(''dist'', v.distancia_km);',
'      APEX_JSON.WRITE(''indice'', v.indice); APEX_JSON.WRITE(''factor'', v.factor_limitante); APEX_JSON.WRITE(''tiempo'', v.tiempo_centro_min);',
'      APEX_JSON.CLOSE_OBJECT;',
'    END LOOP;',
'    APEX_JSON.CLOSE_ARRAY; APEX_JSON.CLOSE_OBJECT;',
'  END LOOP;',
'  APEX_JSON.CLOSE_ARRAY;',
'  v_json := APEX_JSON.GET_CLOB_OUTPUT; v_len := DBMS_LOB.GETLENGTH(v_json);',
'  WHILE v_pos <= v_len LOOP HTP.PRN(DBMS_LOB.SUBSTR(v_json, 8000, v_pos)); v_pos := v_pos + 8000; END LOOP;',
'  APEX_JSON.FREE_OUTPUT;',
'END;'))
,p_process_clob_language=>'PLSQL'
,p_internal_uid=>8900550584000011
);
wwv_flow_imp_page.create_page_process(
 p_id=>wwv_flow_imp.id(8900550584000012)
,p_process_sequence=>10
,p_process_point=>'ON_DEMAND'
,p_process_type=>'NATIVE_PLSQL'
,p_process_name=>'SIMULAR'
,p_static_id=>'simular'
,p_process_sql_clob=>wwv_flow_string.join(wwv_flow_t_varchar2(
'DECLARE v_json CLOB;',
'BEGIN',
'  v_json := WKSP_DATATHON.PV_SIMULA(apex_application.g_x01, NVL(TO_NUMBER(apex_application.g_x02),0), NVL(TO_NUMBER(apex_application.g_x03),0), NVL(TO_NUMBER(apex_application.g_x04),0), NVL(TO_NUMBER(apex_application.g_x05),0), NVL(TO_NUMBER(apex_app'
||'lication.g_x06),0));',
'  HTP.P(v_json);',
'END;'))
,p_process_clob_language=>'PLSQL'
,p_internal_uid=>8900550584000012
);
end;
/
prompt --application/pages/page_00020
begin
wwv_flow_imp_page.create_page(
 p_id=>20
,p_name=>'Perfil Ciudadano'
,p_alias=>'PERFIL-CIUDADANO'
,p_step_title=>'Perfil Ciudadano'
,p_autocomplete_on_off=>'OFF'
,p_step_template=>4073832297226169690
,p_page_template_options=>'#DEFAULT#'
,p_page_is_public_y_n=>'Y'
,p_protection_level=>'C'
,p_page_component_map=>'10'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(8900550584000016)
,p_plug_name=>'Dashboard ciudadano'
,p_static_id=>'dashboard-ciudadano'
,p_region_template_options=>'#DEFAULT#'
,p_plug_template=>4073835273271169698
,p_plug_display_sequence=>10
,p_plug_item_display_point=>'ABOVE'
,p_location=>null
,p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(
'BEGIN HTP.P(q''~<style>',
'.pv20{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#0f172a;max-width:1400px;margin:0 auto}',
'.pv20 .head{display:flex;justify-content:space-between;gap:16px;align-items:flex-end;flex-wrap:wrap;margin:4px 0 16px}',
'.pv20 .kick{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#0f766e;font-weight:800}',
'.pv20 h1{font-size:28px;line-height:1.15;margin:4px 0 4px;color:#0f2a44;letter-spacing:-.02em}',
'.pv20 .sub{font-size:13px;color:#5b6b7c;margin:0;max-width:760px}',
'.pv20 .tag{font-size:11px;background:#eefaf8;border:1px solid #cdeee8;color:#0f766e;border-radius:99px;padding:6px 10px;font-weight:700;white-space:nowrap}',
'.pv20 .grid{display:grid;grid-template-columns:300px minmax(0,1fr);gap:16px;align-items:start}',
'.pv20 .card{background:#fff;border:1px solid #dbe3ea;border-radius:14px;padding:15px;box-shadow:0 1px 2px rgba(15,42,68,.05),0 8px 22px rgba(15,42,68,.06)}',
'.pv20 .panel{position:sticky;top:12px}',
'.pv20 .panel h2{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:#5b6b7c;margin:0 0 12px}',
'.pv20 label{display:block;font-size:12px;font-weight:700;color:#334155;margin:10px 0 4px}',
'.pv20 input[type=range]{width:100%;accent-color:#0f766e}',
'.pv20 .rowlab{display:flex;justify-content:space-between;font-size:11px;color:#5b6b7c;margin-top:2px}',
'.pv20 .chk{display:flex;gap:8px;align-items:flex-start;font-size:12px;font-weight:500;margin:12px 0}',
'.pv20 .chk input{margin-top:2px;accent-color:#0f766e}',
'.pv20 .btn{width:100%;margin-top:12px;background:#0f766e;color:#fff;border:0;border-radius:9px;padding:11px 12px;font-weight:800;cursor:pointer}',
'.pv20 .note{font-size:11px;color:#5b6b7c;line-height:1.45;margin-top:12px;background:#f4f7fa;border:1px solid #e2e8f0;border-radius:9px;padding:9px}',
'.pv20 .kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:14px}',
'.pv20 .kpi{background:#fff;border:1px solid #dbe3ea;border-radius:12px;padding:12px 14px;box-shadow:0 1px 2px rgba(15,42,68,.04)}',
'.pv20 .kpi .l{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#5b6b7c;font-weight:800}',
'.pv20 .kpi b{display:block;font-size:25px;color:#0f2a44;margin-top:3px;letter-spacing:-.02em}',
'.pv20 .kpi .s{font-size:11px;color:#5b6b7c}',
'.pv20 .row{display:grid;grid-template-columns:1.15fr .85fr;gap:14px;margin-top:14px}',
'.pv20 h3{font-size:14px;margin:0 0 10px;color:#0f2a44}',
'.pv20 .svg{display:block;width:100%;height:auto;background:#fbfdff;border:1px solid #eef3f7;border-radius:9px}',
'.pv20 .legend{font-size:10px;color:#64748b;display:flex;gap:12px;margin:4px 0 6px;flex-wrap:wrap}',
'.pv20 .legend i{display:inline-block;width:14px;height:7px;border-radius:2px;margin-right:3px}',
'.pv20 .rank{max-height:430px;overflow:auto;border:1px solid #eef3f7;border-radius:9px}',
'.pv20 table{width:100%;border-collapse:collapse;font-size:11.5px}',
'.pv20 th{position:sticky;top:0;text-align:left;color:#5b6b7c;font-size:10px;text-transform:uppercase;letter-spacing:.05em;background:#f6f9fb;padding:7px 6px;border-bottom:1px solid #dbe3ea;z-index:1}',
'.pv20 td{padding:6px;border-bottom:1px solid #eef2f6}',
'.pv20 tbody tr{cursor:pointer}.pv20 tbody tr:hover{background:#f7fbfb}.pv20 tbody tr.sel{background:#eefaf8}',
'.pv20 .num{text-align:right;font-variant-numeric:tabular-nums}',
'.pv20 .name{font-size:20px;font-weight:800;color:#0f2a44;margin:0}',
'.pv20 .meta{font-size:11.5px;color:#5b6b7c;margin:2px 0 10px}',
'.pv20 .big{font-size:34px;font-weight:800;color:#0f766e;line-height:1}',
'.pv20 .bars{margin:10px 0}',
'.pv20 .bar{display:grid;grid-template-columns:105px 1fr 36px;gap:8px;align-items:center;font-size:11px;margin:6px 0}',
'.pv20 .track{height:7px;background:#eef2f6;border-radius:99px;overflow:hidden}',
'.pv20 .track i{display:block;height:100%;background:#14b8a6;border-radius:99px}',
'.pv20 .stats{display:grid;grid-template-columns:1fr 1fr;gap:6px 10px;font-size:11.5px;margin:10px 0}',
'.pv20 .stats div{display:flex;justify-content:space-between;gap:6px;border-bottom:1px dashed #eef2f6;padding-bottom:3px}',
'.pv20 .stats b{color:#0f2a44}',
'.pv20 .warn{display:block;margin-top:8px;font-size:11px;color:#92400e;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:8px}',
'.pv20 .empty{padding:20px;text-align:center;color:#64748b;font-size:12px}',
'@media(max-width:980px){.pv20 .grid,.pv20 .row{grid-template-columns:1fr}.pv20 .kpis{grid-template-columns:repeat(2,1fr)}.pv20 .panel{position:static}}',
'</style>',
'<div class="pv20">',
'  <div class="head">',
unistr('    <div><div class="kick">Perfil ciudadano</div><h1>Encuentra tu municipio</h1><p class="sub">Ajusta lo que te importa: tiempo a Madrid, precio, servicios, vivienda y empleo. El ranking se recalcula al instante y te explica el porqu\00E9, con la poblaci')
||unistr('\00F3n proyectada a 2035.</p></div>'),
unistr('    <div class="tag">Datos reales \00B7 155 municipios \00B7 proyecci\00F3n 2035</div>'),
'  </div>',
'  <div class="grid">',
'    <aside class="card panel">',
'      <h2>Tus preferencias</h2>',
unistr('      <label>Tiempo m\00E1ximo a Madrid <span class="rowlab"><span></span><b id="v20-time">60 min</b></span></label>'),
'      <input id="f20-time" type="range" min="15" max="120" step="5" value="60">',
unistr('      <label>Distancia m\00E1xima a Sol <span class="rowlab"><span></span><b id="v20-dist">80 km</b></span></label>'),
'      <input id="f20-dist" type="range" min="10" max="100" step="5" value="80">',
unistr('      <label>Precio m\00E1ximo de vivienda <span class="rowlab"><span></span><b id="v20-price">400.000 \20AC</b></span></label>'),
'      <input id="f20-price" type="range" min="60000" max="600000" step="10000" value="400000">',
'      <div class="chk"><input id="f20-missing" type="checkbox"><label for="f20-missing">Incluir municipios sin dato de tiempo o precio</label></div>',
'      <h2 style="margin-top:16px">Pesos</h2>',
unistr('      <label>Demograf\00EDa <span class="rowlab"><span></span><b id="v20-wdem">2</b></span></label><input id="f20-wdem" type="range" min="0" max="5" step="1" value="2">'),
'      <label>Vivienda <span class="rowlab"><span></span><b id="v20-wviv">2</b></span></label><input id="f20-wviv" type="range" min="0" max="5" step="1" value="2">',
'      <label>Servicios <span class="rowlab"><span></span><b id="v20-wser">3</b></span></label><input id="f20-wser" type="range" min="0" max="5" step="1" value="3">',
'      <label>Accesibilidad <span class="rowlab"><span></span><b id="v20-wacc">3</b></span></label><input id="f20-wacc" type="range" min="0" max="5" step="1" value="3">',
'      <label>Empleo <span class="rowlab"><span></span><b id="v20-wemp">2</b></span></label><input id="f20-wemp" type="range" min="0" max="5" step="1" value="2">',
'      <button class="btn" id="f20-run" type="button">Actualizar recomendaciones</button>',
unistr('      <div class="note">El ranking usa los \00EDndices por dimensi\00F3n del dataset real. Los municipios sin dato no se imputan: si no marcas la casilla, se excluyen del filtro.</div>'),
'    </aside>',
'    <section>',
'      <div class="kpis">',
unistr('        <div class="kpi"><div class="l">Municipios que encajan</div><b id="k20-n">\2014</b><div class="s">con tus filtros</div></div>'),
unistr('        <div class="kpi"><div class="l">\00CDndice medio</div><b id="k20-score">\2014</b><div class="s">0-100</div></div>'),
unistr('        <div class="kpi"><div class="l">Mejor tiempo</div><b id="k20-time">\2014</b><div class="s">trayecto directo</div></div>'),
unistr('        <div class="kpi"><div class="l">Precio mediano</div><b id="k20-price">\2014</b><div class="s">vivienda escriturada</div></div>'),
'      </div>',
'      <div class="row">',
'        <div class="card"><h3>Mapa de afinidad</h3><div class="legend"><span><i style="background:#0f766e"></i>65+</span><span><i style="background:#14b8a6"></i>50-65</span><span><i style="background:#5eead4"></i>35-50</span><span><i style="backgroun'
||'d:#bae6fd"></i>&lt;35</span></div><div id="f20-map"></div></div>',
'        <div class="card" id="f20-detail"><h3>Ficha del municipio</h3><div class="empty">Selecciona un municipio en el mapa o en el ranking.</div></div>',
'      </div>',
'      <div class="card" style="margin-top:14px"><h3>Ranking de afinidad</h3><div class="rank"><div id="f20-table"></div></div></div>',
unistr('      <div class="card" style="margin-top:14px"><h3>C\00F3mo leerlo</h3><div style="font-size:12px;color:#334155;line-height:1.55">El \00EDndice de afinidad es la media ponderada de tus pesos sobre las dimensiones del municipio. No es una nota de calidad de ')
||unistr('vida: es una medida de encaje con lo que has pedido. Los precios son precio medio de escritura notarial (\00FAltimos 12 meses) y no incluyen todos los municipios: los que no tienen muestra suficiente aparecen como \00ABsin dato\00BB.</div></div>'),
'    </section>',
'  </div>',
'</div>',
'<script>',
'(function(){',
'  var DATA=[],SELECTED=null;',
'  function $(id){return document.getElementById(id);}',
unistr('  function fmt(v,d){if(v===null||v===undefined||isNaN(v))return ''\2014'';return Number(v).toLocaleString(''es-ES'',{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}'),
'  function esc(s){return String(s).replace(/[&<>"'']/g,function(c){return {''&'':''&amp;'',''<'':''&lt;'',''>'':''&gt;'',''"'':''&quot;'',"''":''&#39;''}[c];});}',
'  function api(name,params,cb){apex.server.process(name,params,{success:function(d){try{cb(typeof d===''string''?JSON.parse(d):d);}catch(e){console.error(e);}},error:function(x){if(!window.__pvTries)window.__pvTries=0;if(window.__pvTries++<8){setTimeou'
||'t(function(){api(name,params,cb);},900);}else{console.error(x);}}});}',
'  function weights(){return [Number($(''f20-wdem'').value),Number($(''f20-wviv'').value),Number($(''f20-wser'').value),Number($(''f20-wacc'').value),Number($(''f20-wemp'').value)];}',
'  function score(m){var w=weights(),sum=w[0]+w[1]+w[2]+w[3]+w[4];if(!sum)return null;return (m.dem*w[0]+m.viv*w[1]+m.ser*w[2]+m.acc*w[3]+m.emp*w[4])/sum;}',
'  function passes(m){var inc=$(''f20-missing'').checked;if(!inc&&(m.tiempo==null||m.precio==null))return false;if(m.tiempo!=null&&m.tiempo>Number($(''f20-time'').value))return false;if(m.dist!=null&&m.dist>Number($(''f20-dist'').value))return false;if(m.pr'
||'ecio!=null&&m.precio>Number($(''f20-price'').value))return false;return true;}',
'  function spark(series,proy){var hist=(series||[]).map(Number);if(!hist.length)return '''';var pr=(proy||[]).map(Number);var all=hist.concat(pr),n=all.length,W=320,H=110,P=14;var mn=Math.min.apply(null,all),mx=Math.max.apply(null,all);function X(i){re'
||'turn P+i/(n-1)*(W-2*P);}function Y(v){return H-P-(v-mn)/((mx-mn)||1)*(H-2*P);}var dh=hist.map(function(v,i){return (i?''L'':''M'')+X(i).toFixed(1)+'',''+Y(v).toFixed(1);}).join('' '');var dp=pr.map(function(v,i){return ''L''+X(hist.length+i).toFixed(1)+'',''+Y(v'
||').toFixed(1);}).join('' '');var x25=X(hist.length-1);var out=''<svg viewBox="0 0 ''+W+'' ''+H+''" style="width:100%;height:auto"><path d="''+dh+''" fill="none" stroke="#0f766e" stroke-width="2"></path>'';if(pr.length){out+=''<path d="M''+x25.toFixed(1)+'',''+Y(his'
||'t[hist.length-1]).toFixed(1)+'' ''+dp+''" fill="none" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4 3"></path>'';}out+=''<line x1="''+x25.toFixed(1)+''" y1="''+P+''" x2="''+x25.toFixed(1)+''" y2="''+(H-P)+''" stroke="#e2e8f0"></line><text x="''+P+''" y="''+('
||'H-2)+''" font-size="9" fill="#64748b">2010</text><text x="''+x25.toFixed(1)+''" y="''+(H-2)+''" font-size="9" fill="#64748b" text-anchor="middle">2025</text>'';if(pr.length){out+=''<text x="''+(W-P)+''" y="''+(H-2)+''" font-size="9" fill="#64748b" text-anchor="'
||'end">2035</text>'';}out+=''</svg>'';return out;}',
unistr('  function drawMap(rows){var pts=rows.filter(function(m){return m.lat!=null&&m.lon!=null;});if(!pts.length){$(''f20-map'').innerHTML=''<div class="empty">Ning\00FAn municipio cumple los filtros.</div>'';return;}var mnLon=Math.min.apply(null,pts.map(function(')
||'m){return m.lon;})),mxLon=Math.max.apply(null,pts.map(function(m){return m.lon;})),mnLat=Math.min.apply(null,pts.map(function(m){return m.lat;})),mxLat=Math.max.apply(null,pts.map(function(m){return m.lat;}));var W=640,H=420,P=20,s=Math.min((W-2*P)/('
||'(mxLon-mnLon)||1),(H-2*P)/((mxLat-mnLat)||1)),ox=(W-(mxLon-mnLon)*s)/2,oy=(H-(mxLat-mnLat)*s)/2,out=[''<svg viewBox="0 0 ''+W+'' ''+H+''" class="svg">''];pts.forEach(function(m){var x=ox+(m.lon-mnLon)*s,y=oy+(mxLat-m.lat)*s,r=3.5+(m.pob||0)/40000*5,c=m._sc'
||'ore>=65?''#0f766e'':m._score>=50?''#14b8a6'':m._score>=35?''#5eead4'':''#bae6fd'',st=m.cod===SELECTED?''#0f172a'':''#ffffff'',sw=m.cod===SELECTED?2.5:1;out.push(''<circle data-cod="''+m.cod+''" cx="''+x.toFixed(1)+''" cy="''+y.toFixed(1)+''" r="''+r.toFixed(1)+''" fill="'
||unistr('''+c+''" stroke="''+st+''" stroke-width="''+sw+''" style="cursor:pointer"><title>''+esc(m.nombre)+'' \00B7 afinidad ''+fmt(m._score,1)+'' \00B7 ''+fmt(m.pob)+'' hab.</title></circle>'');});out.push(''</svg>'');$(''f20-map'').innerHTML=out.join('''');$(''f20-map'').querySelectorA')
||'ll(''circle'').forEach(function(c){c.addEventListener(''click'',function(){SELECTED=c.getAttribute(''data-cod'');render();});});}',
unistr('  function detail(m){if(!m){return ''<h3>Ficha del municipio</h3><div class="empty">Selecciona un municipio en el mapa o en el ranking.</div>'';}var dims=[[''Demograf\00EDa'',m.dem],[''Vivienda'',m.viv],[''Servicios'',m.ser],[''Accesibilidad'',m.acc],[''Empleo'',m.e')
||'mp]];var sorted=dims.slice().sort(function(a,b){return b[1]-a[1];});var good=sorted.slice(0,2).map(function(d){return d[0];}).join('' y '');var bad=sorted.slice(-2).map(function(d){return d[0];}).join('' y '');var bars=dims.map(function(d){return ''<div c'
||'lass="bar"><span>''+d[0]+''</span><div class="track"><i style="width:''+(d[1]||0)+''%"></i></div><b style="text-align:right">''+fmt(d[1],0)+''</b></div>'';}).join('''');return ''<h3>Ficha del municipio</h3><p class="name">''+esc(m.nombre)+''</p><div class="meta"'
||unistr('>''+fmt(m.pob)+'' hab. \00B7 ''+fmt(m.dist,1)+'' km a Sol</div><div class="big">''+fmt(m._score,1)+''</div><div class="meta">\00EDndice de afinidad con tus pesos</div><div class="bars">''+bars+''</div><div class="stats"><div><span>Tiempo al centro</span><b>''+(m.tiem')
||unistr('po==null?''sin dato'':fmt(m.tiempo,0)+'' min'')+''</b></div><div><span>Precio medio</span><b>''+(m.precio==null?''sin dato'':fmt(m.precio,0)+'' \20AC'')+''</b></div><div><span>Precio \20AC/m\00B2</span><b>''+(m.precio_m2==null?''sin dato'':fmt(m.precio_m2,0))+''</b></div><div>')
||unistr('<span>Compraventas</span><b>''+(m.compraventas==null?''sin dato'':fmt(m.compraventas,0))+''</b></div><div><span>Paradas</span><b>''+fmt(m.paradas,0)+''</b></div><div><span>Factor limitante</span><b>''+esc(m.factor||''\2014'')+''</b></div><div><span>Poblaci\00F3n 2035<')
||unistr('/span><b>''+(m.p2035==null?''sin dato'':fmt(m.p2035,0))+''</b></div><div><span>Crecimiento 25-35</span><b>''+(m.crec==null?''sin dato'':(m.crec>0?''+'':'''')+fmt(m.crec,1)+'' %'')+''</b></div></div><div class="meta" style="margin-top:8px">Poblaci\00F3n 2010-2035</div>')
||unistr('''+spark(m.serie||[],m.proy||[])+''<div class="warn">Fortalezas: ''+good+''. A vigilar: ''+bad+''. El precio es media de escritura notarial; un municipio sin muestra suficiente no tiene dato.''+(m.p2035!=null?'' Proyecci\00F3n 2035: ''+fmt(m.p2035,0)+'' hab. (band')
||unistr('a ''+fmt(m.p10,0)+''\2013''+fmt(m.p90,0)+'', fiabilidad ''+esc(m.fiabp||''\2014'')+'').'':'''')+''</div>'';}'),
'  function render(){var rows=DATA.map(function(m){var s=score(m);return Object.assign({},m,{_score:s});}).filter(function(m){return m._score!=null&&passes(m);}).sort(function(a,b){return b._score-a._score;});$(''k20-n'').textContent=rows.length;var avg'
||'=rows.length?rows.reduce(function(a,m){return a+m._score;},0)/rows.length:null;$(''k20-score'').textContent=fmt(avg,1);var times=rows.filter(function(m){return m.tiempo!=null;}).sort(function(a,b){return a.tiempo-b.tiempo;});$(''k20-time'').textContent=t'
||unistr('imes.length?fmt(times[0].tiempo,0)+'' min'':''\2014'';var prices=rows.map(function(m){return m.precio;}).filter(function(v){return v!=null;}).sort(function(a,b){return a-b;});$(''k20-price'').textContent=prices.length?fmt(prices[Math.floor(prices.length/2)],0)')
||unistr('+'' \20AC'':''\2014'';if(!SELECTED||!rows.some(function(m){return m.cod===SELECTED;}))SELECTED=rows.length?rows[0].cod:null;drawMap(rows);var html=''<table><thead><tr><th>#</th><th>Municipio</th><th class="num">Afinidad</th><th class="num">Poblaci\00F3n</th><th class')
||'="num">2035</th><th class="num">Tiempo</th><th class="num">Precio</th></tr></thead><tbody>''+rows.slice(0,20).map(function(m,i){return ''<tr data-cod="''+m.cod+''"''+(m.cod===SELECTED?'' class="sel"'':'''')+''><td class="num">''+(i+1)+''</td><td><b>''+esc(m.nombr'
||unistr('e)+''</b></td><td class="num"><b>''+fmt(m._score,1)+''</b></td><td class="num">''+fmt(m.pob)+''</td><td class="num">''+fmt(m.p2035)+''</td><td class="num">''+(m.tiempo==null?''\2014'':fmt(m.tiempo,0)+'' min'')+''</td><td class="num">''+(m.precio==null?''\2014'':fmt(m.precio')
||unistr(',0)+'' \20AC'')+''</td></tr>'';}).join('''')+''</tbody></table>'';$(''f20-table'').innerHTML=html;$(''f20-table'').querySelectorAll(''tbody tr'').forEach(function(tr){tr.addEventListener(''click'',function(){SELECTED=tr.getAttribute(''data-cod'');render();});});var sel=ro')
||'ws.filter(function(m){return m.cod===SELECTED;})[0];$(''f20-detail'').innerHTML=detail(sel);}',
unistr('  function labels(){ $(''v20-time'').textContent=$(''f20-time'').value+'' min'';$(''v20-dist'').textContent=$(''f20-dist'').value+'' km'';$(''v20-price'').textContent=fmt($(''f20-price'').value,0)+'' \20AC'';$(''v20-wdem'').textContent=$(''f20-wdem'').value;$(''v20-wviv'').text')
||'Content=$(''f20-wviv'').value;$(''v20-wser'').textContent=$(''f20-wser'').value;$(''v20-wacc'').textContent=$(''f20-wacc'').value;$(''v20-wemp'').textContent=$(''f20-wemp'').value;}',
'  function pvBoot(){',
'    [''f20-time'',''f20-dist'',''f20-price'',''f20-wdem'',''f20-wviv'',''f20-wser'',''f20-wacc'',''f20-wemp''].forEach(function(id){$(id).addEventListener(''input'',function(){labels();render();});});',
'    $(''f20-missing'').addEventListener(''change'',render);',
'    $(''f20-run'').addEventListener(''click'',function(){labels();render();});',
'    api(''DATOS'',{},function(rows){DATA=rows;labels();render();});',
'  }',
'(function pvWait(){ if(window.apex && window.apex.server){ setTimeout(pvBoot,1200); } else { setTimeout(pvWait,100); } })();',
'})();',
'</script>~''); END;'))
,p_plug_source_type=>'NATIVE_PLSQL'
);
wwv_flow_imp_page.create_page_process(
 p_id=>wwv_flow_imp.id(8900550584000015)
,p_process_sequence=>10
,p_process_point=>'ON_DEMAND'
,p_process_type=>'NATIVE_PLSQL'
,p_process_name=>'DATOS'
,p_static_id=>'datos'
,p_process_sql_clob=>wwv_flow_string.join(wwv_flow_t_varchar2(
'DECLARE',
'  v_json CLOB; v_len PLS_INTEGER; v_pos PLS_INTEGER := 1;',
'BEGIN',
'  APEX_JSON.INITIALIZE_CLOB_OUTPUT; APEX_JSON.OPEN_ARRAY;',
'  FOR m IN (SELECT * FROM WKSP_DATATHON.PV_MUN_2035 ORDER BY nombre) LOOP',
'    APEX_JSON.OPEN_OBJECT;',
'    APEX_JSON.WRITE(''cod'', m.cod_ine); APEX_JSON.WRITE(''nombre'', m.nombre); APEX_JSON.WRITE(''pob'', m.poblacion);',
'    APEX_JSON.WRITE(''lat'', m.lat); APEX_JSON.WRITE(''lon'', m.lon); APEX_JSON.WRITE(''dist'', m.distancia_sol_km);',
'    APEX_JSON.WRITE(''tiempo'', m.tiempo_centro_min); APEX_JSON.WRITE(''modo'', m.modo); APEX_JSON.WRITE(''paradas'', m.paradas_total);',
'    APEX_JSON.WRITE(''escuelas'', m.escuelas); APEX_JSON.WRITE(''precio'', m.precio_medio); APEX_JSON.WRITE(''precio_m2'', m.precio_m2);',
'    APEX_JSON.WRITE(''compraventas'', m.compraventas); APEX_JSON.WRITE(''fiabilidad'', m.fiabilidad);',
'    APEX_JSON.WRITE(''dem'', m.dim_dem); APEX_JSON.WRITE(''viv'', m.dim_viv); APEX_JSON.WRITE(''ser'', m.dim_ser);',
'    APEX_JSON.WRITE(''acc'', m.dim_acc); APEX_JSON.WRITE(''emp'', m.dim_emp); APEX_JSON.WRITE(''indice'', m.indice);',
'    APEX_JSON.WRITE(''factor'', m.factor_limitante);',
'    APEX_JSON.WRITE(''p2035'', m.poblacion_2035); APEX_JSON.WRITE(''p10'', m.pob_2035_p10); APEX_JSON.WRITE(''p90'', m.pob_2035_p90);',
'    APEX_JSON.WRITE(''crec'', m.crecimiento_pct); APEX_JSON.WRITE(''esc'', m.escenario); APEX_JSON.WRITE(''fiabp'', m.fiab_pronostico);',
'    APEX_JSON.WRITE(''tasa'', m.tasa_2035_pct); APEX_JSON.WRITE(''conv'', m.pob_2035_convergencia); APEX_JSON.WRITE(''pers'', m.pob_2035_persistencia);',
'    APEX_JSON.WRITE(''san25'', m.hab_sanit_2025); APEX_JSON.WRITE(''san35'', m.hab_sanit_2035);',
'    APEX_JSON.WRITE(''edu25'', m.hab_escuela_2025); APEX_JSON.WRITE(''edu35'', m.hab_escuela_2035);',
'    APEX_JSON.WRITE(''par25'', m.hab_parada_2025); APEX_JSON.WRITE(''par35'', m.hab_parada_2035);',
'    APEX_JSON.WRITE(''viv25'', m.hab_vivienda_2025); APEX_JSON.WRITE(''viv35'', m.hab_vivienda_2035);',
'    APEX_JSON.OPEN_ARRAY(''serie'');',
'    FOR s IN (SELECT poblacion FROM WKSP_DATATHON.PV_SERIE WHERE cod_ine=m.cod_ine ORDER BY anio) LOOP APEX_JSON.WRITE(s.poblacion); END LOOP;',
'    APEX_JSON.CLOSE_ARRAY;',
'    APEX_JSON.OPEN_ARRAY(''proy'');',
'    FOR s IN (SELECT poblacion FROM WKSP_DATATHON.PV_PROYECCION_SERIE WHERE cod_ine=m.cod_ine ORDER BY anio) LOOP APEX_JSON.WRITE(s.poblacion); END LOOP;',
'    APEX_JSON.CLOSE_ARRAY;',
'    APEX_JSON.OPEN_ARRAY(''vecinos'');',
'    FOR v IN (SELECT v.nombre_vecino, v.distancia_km, b.indice, b.factor_limitante, b.tiempo_centro_min',
'              FROM WKSP_DATATHON.PV_VECINOS v JOIN WKSP_DATATHON.PV_MUN_BASE b ON b.cod_ine=v.cod_vecino',
'              WHERE v.cod_ine=m.cod_ine ORDER BY v.distancia_km) LOOP',
'      APEX_JSON.OPEN_OBJECT; APEX_JSON.WRITE(''nombre'', v.nombre_vecino); APEX_JSON.WRITE(''dist'', v.distancia_km);',
'      APEX_JSON.WRITE(''indice'', v.indice); APEX_JSON.WRITE(''factor'', v.factor_limitante); APEX_JSON.WRITE(''tiempo'', v.tiempo_centro_min);',
'      APEX_JSON.CLOSE_OBJECT;',
'    END LOOP;',
'    APEX_JSON.CLOSE_ARRAY; APEX_JSON.CLOSE_OBJECT;',
'  END LOOP;',
'  APEX_JSON.CLOSE_ARRAY;',
'  v_json := APEX_JSON.GET_CLOB_OUTPUT; v_len := DBMS_LOB.GETLENGTH(v_json);',
'  WHILE v_pos <= v_len LOOP HTP.PRN(DBMS_LOB.SUBSTR(v_json, 8000, v_pos)); v_pos := v_pos + 8000; END LOOP;',
'  APEX_JSON.FREE_OUTPUT;',
'END;'))
,p_process_clob_language=>'PLSQL'
,p_internal_uid=>8900550584000015
);
end;
/
prompt --application/pages/page_00030
begin
wwv_flow_imp_page.create_page(
 p_id=>30
,p_name=>'Datos'
,p_alias=>'DATOS'
,p_step_title=>'Datos'
,p_autocomplete_on_off=>'OFF'
,p_step_template=>4073832297226169690
,p_page_template_options=>'#DEFAULT#'
,p_page_is_public_y_n=>'Y'
,p_protection_level=>'C'
,p_page_component_map=>'10'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(8900550584000019)
,p_plug_name=>'Tablas de datos'
,p_static_id=>'tablas-de-datos'
,p_region_template_options=>'#DEFAULT#'
,p_plug_template=>4073835273271169698
,p_plug_display_sequence=>10
,p_plug_item_display_point=>'ABOVE'
,p_location=>null
,p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(
'BEGIN HTP.P(q''~<style>',
'.pv30{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#0f172a;max-width:1400px;margin:0 auto}',
'.pv30 .head{display:flex;justify-content:space-between;gap:16px;align-items:flex-end;flex-wrap:wrap;margin:4px 0 16px}',
'.pv30 .kick{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#0f766e;font-weight:800}',
'.pv30 h1{font-size:28px;line-height:1.15;margin:4px 0 4px;color:#0f2a44;letter-spacing:-.02em}',
'.pv30 .sub{font-size:13px;color:#5b6b7c;margin:0;max-width:820px}',
'.pv30 .tag{font-size:11px;background:#eefaf8;border:1px solid #cdeee8;color:#0f766e;border-radius:99px;padding:6px 10px;font-weight:700;white-space:nowrap}',
'.pv30 .card{background:#fff;border:1px solid #dbe3ea;border-radius:14px;padding:15px;box-shadow:0 1px 2px rgba(15,42,68,.05),0 8px 22px rgba(15,42,68,.06);margin-bottom:14px}',
'.pv30 .kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:14px}',
'.pv30 .kpi{background:#fff;border:1px solid #dbe3ea;border-radius:12px;padding:12px 14px}',
'.pv30 .kpi .l{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#5b6b7c;font-weight:800}',
'.pv30 .kpi b{display:block;font-size:24px;color:#0f2a44;margin-top:3px;letter-spacing:-.02em}',
'.pv30 .kpi .s{font-size:11px;color:#5b6b7c}',
'.pv30 h3{font-size:14px;margin:0 0 10px;color:#0f2a44}',
'.pv30 .tools{display:flex;gap:10px;align-items:flex-end;flex-wrap:wrap;margin-bottom:10px}',
'.pv30 .tools label{font-size:11px;font-weight:700;color:#334155;display:block;margin-bottom:3px}',
'.pv30 input,.pv30 select{padding:8px 9px;border:1px solid #cbd5e1;border-radius:8px;font:inherit;font-size:12px;background:#fff;color:#0f172a}',
'.pv30 .btn{background:#0f766e;color:#fff;border:0;border-radius:9px;padding:9px 13px;font-weight:800;font-size:12px;cursor:pointer}',
'.pv30 .btn.ghost{background:#fff;color:#0f766e;border:1px solid #99e0d6}',
'.pv30 .wrap{overflow:auto;max-height:560px;border:1px solid #eef3f7;border-radius:9px}',
'.pv30 table{width:100%;border-collapse:collapse;font-size:11.5px}',
'.pv30 th{position:sticky;top:0;text-align:left;color:#5b6b7c;font-size:10px;text-transform:uppercase;letter-spacing:.05em;background:#f6f9fb;padding:7px 6px;border-bottom:1px solid #dbe3ea;z-index:1;white-space:nowrap;cursor:pointer;user-select:none}',
'.pv30 th:hover{color:#0f766e}',
'.pv30 td{padding:6px;border-bottom:1px solid #eef2f6;white-space:nowrap}',
'.pv30 td.name{white-space:normal;min-width:150px}',
'.pv30 .num{text-align:right;font-variant-numeric:tabular-nums}',
'.pv30 .pill{display:inline-block;font-size:10px;font-weight:800;border-radius:99px;padding:2px 7px}',
'.pv30 .p-fuerte{background:#d7f5f0;color:#0f766e}',
'.pv30 .p-mod{background:#e6f4fb;color:#0369a1}',
'.pv30 .p-est{background:#fef3c7;color:#92400e}',
'.pv30 .p-dec{background:#fee2e2;color:#b91c1c}',
'.pv30 .fiab{font-size:10px;font-weight:700;color:#475569}',
'.pv30 .note{font-size:11px;color:#5b6b7c;line-height:1.5;background:#f4f7fa;border:1px solid #e2e8f0;border-radius:9px;padding:9px;margin-top:10px}',
'.pv30 .warn{font-size:11px;color:#92400e;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:8px;margin-top:10px}',
'.pv30 .muted{color:#94a3b8}',
'@media(max-width:980px){.pv30 .kpis{grid-template-columns:repeat(2,1fr)}}',
'</style>',
'<div class="pv30">',
'  <div class="head">',
unistr('    <div><div class="kick">Datos abiertos</div><h1>Tablas de datos</h1><p class="sub">Los 155 municipios con sus indicadores actuales y la proyecci\00F3n a 2035. Puedes buscar, ordenar por cualquier columna y descargar el resultado en CSV.</p></div>'),
unistr('    <div class="tag">155 municipios \00B7 26 a\00F1os de serie</div>'),
'  </div>',
'',
'  <div class="kpis">',
unistr('    <div class="kpi"><div class="l">Municipios</div><b id="k30-n">\2014</b><div class="s">visibles con el filtro</div></div>'),
unistr('    <div class="kpi"><div class="l">Poblaci\00F3n 2025</div><b id="k30-p25">\2014</b><div class="s">padr\00F3n</div></div>'),
unistr('    <div class="kpi"><div class="l">Poblaci\00F3n 2035</div><b id="k30-p35">\2014</b><div class="s">proyecci\00F3n</div></div>'),
unistr('    <div class="kpi"><div class="l">Crecimiento medio municipal</div><b id="k30-crec">\2014</b><div class="s">2025-2035</div></div>'),
'  </div>',
'',
'  <div class="card">',
'    <h3>Municipios e indicadores</h3>',
'    <div class="tools">',
'      <div><label for="f30-q">Buscar municipio</label><input id="f30-q" type="search" placeholder="Nombre..." style="min-width:220px"></div>',
'      <div><label for="f30-esc">Escenario</label><select id="f30-esc"><option value="">Todos</option><option>Crecimiento fuerte</option><option>Crecimiento moderado</option><option>Estancamiento</option><option>Declive</option></select></div>',
'      <div><label for="f30-fiab">Fiabilidad</label><select id="f30-fiab"><option value="">Todas</option><option>Alta</option><option>Media</option><option>Baja</option></select></div>',
'      <button class="btn ghost" id="f30-csv" type="button">Descargar CSV</button>',
'    </div>',
'    <div class="wrap"><div id="f30-table"></div></div>',
unistr('    <div class="note" id="f30-count">\2014</div>'),
'  </div>',
'',
'  <div class="card">',
'    <h3>Serie agregada de los 155 municipios, 2010-2035</h3>',
'    <div class="wrap" style="max-height:560px"><div id="f30-serie"></div></div>',
unistr('    <div class="warn">2010-2025 es poblaci\00F3n observada (padr\00F3n). 2026-2035 es proyecci\00F3n del modelo tendencial anclado al crecimiento oficial de la Comunidad de Madrid. La fila de 2026 marca el cambio de fuente.</div>'),
'  </div>',
'',
'  <div class="card">',
'    <h3>Diccionario y fuentes</h3>',
'    <div class="note">',
unistr('      <b>Poblaci\00F3n 2025:</b> padr\00F3n municipal (INE, cifras oficiales).<br>'),
unistr('      <b>Poblaci\00F3n 2035:</b> modelo propio. Tendencia logar\00EDtmica 2015-2025, convergencia amortiguada a la mitad en 10 a\00F1os y anclaje al crecimiento oficial de la CAM (7.137.031 en 2025 a 7.937.124 en 2035, IESTADIS/INE).<br>'),
unistr('      <b>Banda:</b> intervalo de predicci\00F3n del 80 % de la regresi\00F3n, que recoge la volatilidad hist\00F3rica de cada municipio.<br>'),
unistr('      <b>Fiabilidad:</b> alta si el municipio tiene 5.000 habitantes o m\00E1s y R2 igual o mayor que 0,6; media si tiene 1.000 o m\00E1s o R2 igual o mayor que 0,3; baja en el resto.<br>'),
unistr('      <b>\00CDndice:</b> \00EDndice compuesto 2025 del proyecto (20 % demograf\00EDa, 15 % vivienda, 25 % servicios, 25 % accesibilidad, 15 % empleo).<br>'),
unistr('      <b>Presi\00F3n:</b> habitantes por equipamiento si la oferta no cambia. Sanidad = centros de salud + consultorios (2024). Vivienda = unidades urbanas residenciales del Catastro (2025). No se proyecta la oferta.<br>'),
unistr('      <b>Precio:</b> precio medio de escritura notarial (Notariado v\00EDa S\00F3kerim, CC-BY). Sin muestra suficiente queda vac\00EDo.<br>'),
'      <b>Tiempo:</b> percentil 10 de trayectos directos a menos de 5 km de Sol (GTFS CRTM). Solo 56 de 155 municipios tienen trayecto directo.<br>',
unistr('      <b>Licencia:</b> CC-BY. Atribuci\00F3n CRTM: Powered by CRTM.'),
'    </div>',
'  </div>',
'</div>',
'<script>',
'(function(){',
'  var DATA=[],VIEW=[],SORT={k:''nombre'',dir:1};',
unistr('  var COLS=[[''nombre'',''Municipio''],[''pob'',''Poblaci\00F3n 2025''],[''p2035'',''Poblaci\00F3n 2035''],[''crec'',''Crec. %''],[''banda'',''Banda 80 %''],[''esc'',''Escenario''],[''fiabp'',''Fiabilidad''],[''indice'',''\00CDndice 2025''],[''tiempo'',''Tiempo''],[''precio'',''Precio''],[''san35'',''Hab')
||'./equip. sanitario''],[''viv35'',''Hab./vivienda'']];',
'  function $(id){return document.getElementById(id);}',
unistr('  function fmt(v,d){if(v===null||v===undefined||isNaN(v))return ''\2014'';return Number(v).toLocaleString(''es-ES'',{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}'),
'  function esc(s){return String(s).replace(/[&<>"'']/g,function(c){return {''&'':''&amp;'',''<'':''&lt;'',''>'':''&gt;'',''"'':''&quot;'',"''":''&#39;''}[c];});}',
'  function api(name,params,cb){apex.server.process(name,params,{success:function(d){try{cb(typeof d===''string''?JSON.parse(d):d);}catch(e){console.error(e);}},error:function(x){if(!window.__pvTries)window.__pvTries=0;if(window.__pvTries++<8){setTimeou'
||'t(function(){api(name,params,cb);},900);}else{console.error(x);}}});}',
unistr('  function pill(e){var c=e===''Crecimiento fuerte''?''p-fuerte'':e===''Crecimiento moderado''?''p-mod'':e===''Declive''?''p-dec'':''p-est'';return ''<span class="pill ''+c+''">''+esc(e||''\2014'')+''</span>'';}'),
'  function filtered(){var q=$(''f30-q'').value.trim().toLowerCase(),e=$(''f30-esc'').value,f=$(''f30-fiab'').value;return DATA.filter(function(m){if(q&&m.nombre.toLowerCase().indexOf(q)<0)return false;if(e&&m.esc!==e)return false;if(f&&m.fiabp!==f)return f'
||'alse;return true;});}',
'  function sorted(rows){var k=SORT.k,d=SORT.dir;return rows.slice().sort(function(a,b){var va=a[k],vb=b[k];if(va==null&&vb==null)return 0;if(va==null)return 1;if(vb==null)return -1;if(typeof va===''string'')return va.localeCompare(vb,''es'')*d;return (va'
||'-vb)*d;});}',
unistr('  function renderTable(){VIEW=sorted(filtered());var head=''<table><thead><tr>''+COLS.map(function(c){var arr=SORT.k===c[0]?(SORT.dir>0?'' \25B2'':'' \25BC''):'''';var cls=(c[0]===''nombre'')?'''':'' class="num"'';return ''<th data-k="''+c[0]+''"''+cls+''>''+c[1]+arr+''</th>'';})')
||'.join('''')+''</tr></thead><tbody>'';var body=VIEW.map(function(m){return ''<tr><td class="name"><b>''+esc(m.nombre)+''</b></td><td class="num">''+fmt(m.pob)+''</td><td class="num"><b>''+fmt(m.p2035)+''</b></td><td class="num">''+(m.crec>0?''+'':'''')+fmt(m.crec,1)+'
||unistr(''' %</td><td class="num muted">''+fmt(m.p10)+'' \2013 ''+fmt(m.p90)+''</td><td>''+pill(m.esc)+''</td><td class="fiab">''+esc(m.fiabp||''\2014'')+''</td><td class="num">''+fmt(m.indice,1)+''</td><td class="num">''+(m.tiempo==null?''\2014'':fmt(m.tiempo,0)+'' min'')+''</td><td class')
||unistr('="num">''+(m.precio==null?''\2014'':fmt(m.precio,0)+'' \20AC'')+''</td><td class="num">''+fmt(m.san35,0)+''</td><td class="num">''+fmt(m.viv35,2)+''</td></tr>'';}).join('''');$(''f30-table'').innerHTML=head+body+''</tbody></table>'';$(''f30-table'').querySelectorAll(''th'').forE')
||'ach(function(th){th.addEventListener(''click'',function(){var k=th.getAttribute(''data-k'');if(SORT.k===k)SORT.dir*=-1;else{SORT.k=k;SORT.dir=1;}renderTable();});});var n=VIEW.length,p25=0,p35=0,c=0,nc=0;VIEW.forEach(function(m){p25+=m.pob||0;p35+=m.p203'
||unistr('5||0;if(m.crec!=null){c+=m.crec;nc++;}});$(''k30-n'').textContent=n;$(''k30-p25'').textContent=fmt(p25);$(''k30-p35'').textContent=fmt(p35);$(''k30-crec'').textContent=nc?(c/nc>0?''+'':'''')+fmt(c/nc,1)+'' %'':''\2014'';$(''f30-count'').textContent=n+'' de ''+DATA.length+'' ')
||unistr('municipios \00B7 ordenado por ''+COLS.filter(function(x){return x[0]===SORT.k;})[0][1]+(SORT.dir>0?'' (ascendente)'':'' (descendente)'');}'),
'  function renderSerie(){if(!DATA.length)return;var years=[],tot={};for(var y=2010;y<=2035;y++){years.push(y);tot[y]=0;}DATA.forEach(function(m){(m.serie||[]).forEach(function(v,i){tot[2010+i]+=Number(v)||0;});(m.proy||[]).forEach(function(v,i){tot[2'
||unistr('026+i]+=Number(v)||0;});});var rows=years.map(function(y,i){var prev=i?tot[years[i-1]]:null;var g=prev?(tot[y]/prev-1)*100:null;return ''<tr><td>''+y+(y===2026?'' <span class="pill p-mod">proyecci\00F3n</span>'':'''')+''</td><td class="num"><b>''+fmt(tot[y])+''</')
||unistr('b></td><td class="num">''+(g==null?''\2014'':(g>0?''+'':'''')+fmt(g,2)+'' %'')+''</td></tr>'';}).join('''');$(''f30-serie'').innerHTML=''<table><thead><tr><th>A\00F1o</th><th class="num">Poblaci\00F3n de los 155</th><th class="num">Variaci\00F3n anual</th></tr></thead><tbody>''+rows')
||'+''</tbody></table>'';}',
'  function csv(){var sep='';'';var lines=[[''Municipio'',''Poblacion 2025'',''Poblacion 2035'',''P10'',''P90'',''Crecimiento %'',''Escenario'',''Fiabilidad'',''Indice 2025'',''Tiempo min'',''Precio euros'',''Hab por equipamiento sanitario 2035'',''Hab por vivienda 2035''].join('
||'sep)];function num(v,d){if(v==null||v===''''||isNaN(v))return '''';return Number(v).toFixed(d==null?0:d).replace(''.'','','');}VIEW.forEach(function(m){lines.push([m.nombre,num(m.pob),num(m.p2035),num(m.p10),num(m.p90),num(m.crec,1),m.esc,m.fiabp,num(m.indic'
||'e,1),num(m.tiempo,0),num(m.precio,0),num(m.san35,0),num(m.viv35,2)].join(sep));});var blob=new Blob([''\ufeff''+lines.join(''\r\n'')],{type:''text/csv;charset=utf-8''});var a=document.createElement(''a'');a.href=URL.createObjectURL(blob);a.download=''pueblos_'
||'con_vida_2035.csv'';document.body.appendChild(a);a.click();document.body.removeChild(a);}',
'  function boot(){$(''f30-q'').addEventListener(''input'',renderTable);$(''f30-esc'').addEventListener(''change'',renderTable);$(''f30-fiab'').addEventListener(''change'',renderTable);$(''f30-csv'').addEventListener(''click'',csv);api(''DATOS'',{},function(rows){DATA='
||'rows;renderTable();renderSerie();});}',
'  (function pvWait(){ if(window.apex && window.apex.server){ setTimeout(boot,1200); } else { setTimeout(pvWait,100); } })();',
'})();',
'</script>',
'~''); END;'))
,p_plug_source_type=>'NATIVE_PLSQL'
);
wwv_flow_imp_page.create_page_process(
 p_id=>wwv_flow_imp.id(8900550584000018)
,p_process_sequence=>10
,p_process_point=>'ON_DEMAND'
,p_process_type=>'NATIVE_PLSQL'
,p_process_name=>'DATOS'
,p_static_id=>'datos'
,p_process_sql_clob=>wwv_flow_string.join(wwv_flow_t_varchar2(
'DECLARE',
'  v_json CLOB; v_len PLS_INTEGER; v_pos PLS_INTEGER := 1;',
'BEGIN',
'  APEX_JSON.INITIALIZE_CLOB_OUTPUT; APEX_JSON.OPEN_ARRAY;',
'  FOR m IN (SELECT * FROM WKSP_DATATHON.PV_MUN_2035 ORDER BY nombre) LOOP',
'    APEX_JSON.OPEN_OBJECT;',
'    APEX_JSON.WRITE(''cod'', m.cod_ine); APEX_JSON.WRITE(''nombre'', m.nombre); APEX_JSON.WRITE(''pob'', m.poblacion);',
'    APEX_JSON.WRITE(''lat'', m.lat); APEX_JSON.WRITE(''lon'', m.lon); APEX_JSON.WRITE(''dist'', m.distancia_sol_km);',
'    APEX_JSON.WRITE(''tiempo'', m.tiempo_centro_min); APEX_JSON.WRITE(''modo'', m.modo); APEX_JSON.WRITE(''paradas'', m.paradas_total);',
'    APEX_JSON.WRITE(''escuelas'', m.escuelas); APEX_JSON.WRITE(''precio'', m.precio_medio); APEX_JSON.WRITE(''precio_m2'', m.precio_m2);',
'    APEX_JSON.WRITE(''compraventas'', m.compraventas); APEX_JSON.WRITE(''fiabilidad'', m.fiabilidad);',
'    APEX_JSON.WRITE(''dem'', m.dim_dem); APEX_JSON.WRITE(''viv'', m.dim_viv); APEX_JSON.WRITE(''ser'', m.dim_ser);',
'    APEX_JSON.WRITE(''acc'', m.dim_acc); APEX_JSON.WRITE(''emp'', m.dim_emp); APEX_JSON.WRITE(''indice'', m.indice);',
'    APEX_JSON.WRITE(''factor'', m.factor_limitante);',
'    APEX_JSON.WRITE(''p2035'', m.poblacion_2035); APEX_JSON.WRITE(''p10'', m.pob_2035_p10); APEX_JSON.WRITE(''p90'', m.pob_2035_p90);',
'    APEX_JSON.WRITE(''crec'', m.crecimiento_pct); APEX_JSON.WRITE(''esc'', m.escenario); APEX_JSON.WRITE(''fiabp'', m.fiab_pronostico);',
'    APEX_JSON.WRITE(''tasa'', m.tasa_2035_pct); APEX_JSON.WRITE(''conv'', m.pob_2035_convergencia); APEX_JSON.WRITE(''pers'', m.pob_2035_persistencia);',
'    APEX_JSON.WRITE(''san25'', m.hab_sanit_2025); APEX_JSON.WRITE(''san35'', m.hab_sanit_2035);',
'    APEX_JSON.WRITE(''edu25'', m.hab_escuela_2025); APEX_JSON.WRITE(''edu35'', m.hab_escuela_2035);',
'    APEX_JSON.WRITE(''par25'', m.hab_parada_2025); APEX_JSON.WRITE(''par35'', m.hab_parada_2035);',
'    APEX_JSON.WRITE(''viv25'', m.hab_vivienda_2025); APEX_JSON.WRITE(''viv35'', m.hab_vivienda_2035);',
'    APEX_JSON.OPEN_ARRAY(''serie'');',
'    FOR s IN (SELECT poblacion FROM WKSP_DATATHON.PV_SERIE WHERE cod_ine=m.cod_ine ORDER BY anio) LOOP APEX_JSON.WRITE(s.poblacion); END LOOP;',
'    APEX_JSON.CLOSE_ARRAY;',
'    APEX_JSON.OPEN_ARRAY(''proy'');',
'    FOR s IN (SELECT poblacion FROM WKSP_DATATHON.PV_PROYECCION_SERIE WHERE cod_ine=m.cod_ine ORDER BY anio) LOOP APEX_JSON.WRITE(s.poblacion); END LOOP;',
'    APEX_JSON.CLOSE_ARRAY;',
'    APEX_JSON.OPEN_ARRAY(''vecinos'');',
'    FOR v IN (SELECT v.nombre_vecino, v.distancia_km, b.indice, b.factor_limitante, b.tiempo_centro_min',
'              FROM WKSP_DATATHON.PV_VECINOS v JOIN WKSP_DATATHON.PV_MUN_BASE b ON b.cod_ine=v.cod_vecino',
'              WHERE v.cod_ine=m.cod_ine ORDER BY v.distancia_km) LOOP',
'      APEX_JSON.OPEN_OBJECT; APEX_JSON.WRITE(''nombre'', v.nombre_vecino); APEX_JSON.WRITE(''dist'', v.distancia_km);',
'      APEX_JSON.WRITE(''indice'', v.indice); APEX_JSON.WRITE(''factor'', v.factor_limitante); APEX_JSON.WRITE(''tiempo'', v.tiempo_centro_min);',
'      APEX_JSON.CLOSE_OBJECT;',
'    END LOOP;',
'    APEX_JSON.CLOSE_ARRAY; APEX_JSON.CLOSE_OBJECT;',
'  END LOOP;',
'  APEX_JSON.CLOSE_ARRAY;',
'  v_json := APEX_JSON.GET_CLOB_OUTPUT; v_len := DBMS_LOB.GETLENGTH(v_json);',
'  WHILE v_pos <= v_len LOOP HTP.PRN(DBMS_LOB.SUBSTR(v_json, 8000, v_pos)); v_pos := v_pos + 8000; END LOOP;',
'  APEX_JSON.FREE_OUTPUT;',
'END;'))
,p_process_clob_language=>'PLSQL'
,p_internal_uid=>8900550584000018
);
end;
/
prompt --application/deployment/definition
begin
wwv_flow_imp.g_varchar2_table := wwv_flow_imp.empty_varchar2_table;
wwv_flow_imp_shared.create_install(
 p_id=>wwv_flow_imp.id(10237754273234617)
,p_deinstall_script_clob=>wwv_flow_imp.varchar2_to_clob(wwv_flow_imp.g_varchar2_table)
);
end;
/
prompt --application/deployment/checks
begin
null;
end;
/
prompt --application/deployment/buildoptions
begin
null;
end;
/
prompt --application/end_environment
begin
wwv_flow_imp.import_end(p_auto_install_sup_obj => nvl(wwv_flow_application_install.get_auto_install_sup_obj, false)
);
commit;
end;
/
set verify on feedback on define on
prompt  ...done
