<?php
/**
 * Plugin Name: CCTV Video Directory
 * Description: Searchable Claremont CCTV library with meeting navigator links, local caching and safe background refreshes. Shortcode: [cctv_directory]
 * Version: 1.0.0
 * Requires at least: 6.2
 * Requires PHP: 7.4
 * Author: Kevin Tyson
 * License: GPL-2.0-or-later
 */
if (!defined('ABSPATH')) { exit; }
const CCTV_DIR_SOURCE = 'https://reflect-claremont.cablecast.tv';
const CCTV_DIR_NAV = 'https://csbmn.claremontv.org/';
function cctv_dir_seed() { static $seed; if (!$seed) {$seed=json_decode(file_get_contents(__DIR__.'/assets/catalog.json'),true);} return $seed; }
function cctv_dir_catalog() { $c=get_option('cctv_dir_catalog');return is_array($c)&&!empty($c['rows'])?$c:cctv_dir_seed(); }
function cctv_dir_activate() { if (!wp_next_scheduled('cctv_dir_daily')) {wp_schedule_event(time()+300,'daily','cctv_dir_daily');} }
function cctv_dir_deactivate() {wp_clear_scheduled_hook('cctv_dir_daily');wp_clear_scheduled_hook('cctv_dir_step');delete_option('cctv_dir_job');delete_option('cctv_dir_lock');}
register_activation_hook(__FILE__,'cctv_dir_activate');register_deactivation_hook(__FILE__,'cctv_dir_deactivate');
function cctv_dir_http($url) {
 $host=wp_parse_url($url,PHP_URL_HOST);if(!in_array($host,array('reflect-claremont.cablecast.tv','csbmn.claremontv.org'),true)) {throw new Exception('Unexpected source host.');}
 $r=wp_safe_remote_get($url,array('timeout'=>12,'redirection'=>2,'limit_response_size'=>3000000));
 if(is_wp_error($r)||wp_remote_retrieve_response_code($r)!==200){throw new Exception('A source could not be reached. The previous directory is unchanged.');}
 return wp_remote_retrieve_body($r);
}
function cctv_dir_source($path) {
 $html=cctv_dir_http(CCTV_DIR_SOURCE.$path);
 if(!preg_match('/window\.__remixContext = (.*?);<\/script>/s',$html,$m)){throw new Exception('CCTV changed its catalog format.');}
 $data=json_decode($m[1],true);if(empty($data['state']['loaderData'])){throw new Exception('Invalid CCTV data.');}return $data['state']['loaderData'];
}
function cctv_dir_start() {
 if(get_option('cctv_dir_job')){return;}
 if(add_option('cctv_dir_job',array('phase'=>'discover','site'=>1,'groups'=>array(),'queue'=>array(),'rows'=>array(),'received'=>array(),'seen'=>array(),'links'=>array(),'done'=>0,'started'=>time()),'','no')) {
 update_option('cctv_dir_status',array('message'=>'Refreshing from CCTV…','running'=>true,'at'=>time()),false);
 if(!wp_next_scheduled('cctv_dir_step')){wp_schedule_single_event(time()+5,'cctv_dir_step');}
 }
}
add_action('cctv_dir_daily','cctv_dir_start');add_action('cctv_dir_step','cctv_dir_step');
function cctv_dir_primary_ids($html) {
 $region=$html;if(preg_match('/<header\b[^>]*>(.*?)<\/header>/is',$html,$m)){$region=$m[1];}
 if(preg_match('/<dt>\s*Recording\s*<\/dt>\s*<dd>(.*?)<\/dd>/is',$region,$r)&&preg_match('~https://reflect-claremont\.cablecast\.tv/internetchannel/show/(\d+)~',$r[1],$m)){return array((int)$m[1]);}
 preg_match_all('~https://reflect-claremont\.cablecast\.tv/internetchannel/show/(\d+)~',$region,$m);return array_values(array_unique(array_map('intval',$m[1])));
}
function cctv_dir_step() {
 $lock=(int)get_option('cctv_dir_lock');if($lock&&$lock<time()-180){delete_option('cctv_dir_lock');}
 if(!add_option('cctv_dir_lock',time(),'','no')){return;}
 try {
 $job=get_option('cctv_dir_job');if(!$job){return;}
 if($job['phase']==='discover') {
  $site=$job['site'];$data=cctv_dir_source('/internetchannel?site='.$site);$groups=$data['root']['site']['galleries']??null;
  if(!is_array($groups)||!count($groups)){throw new Exception('CCTV returned no collections.');}
  foreach($groups as $g){$id=(int)$g['cablecastGalleryId'];$job['groups'][$id]=array('id'=>$id,'title'=>$g['title'],'site'=>$site,'channel'=>$site===1?8:10);$job['queue'][]=array($id,1);}
  if($site===1){$job['site']=2;}else{$job['phase']='galleries';}
 } elseif($job['phase']==='galleries') {
  $task=array_shift($job['queue']);$id=$task[0];$page=$task[1];$g=$job['groups'][$id];
  $d=cctv_dir_source('/internetchannel/gallery/'.$id.'?site='.$g['site'].'&page='.$page);$gallery=$d['routes/_shell.gallery.$galleryId']['gallery']??null;
  if(!is_array($gallery)||!isset($gallery['shows'],$gallery['meta']['count'],$gallery['meta']['pageSize'])||$gallery['meta']['pageSize']<1){throw new Exception('Invalid gallery page.');}
  $count=(int)$gallery['meta']['count'];$size=(int)$gallery['meta']['pageSize'];
  if($page===1){$job['groups'][$id]['sourceCount']=$count;$pages=(int)ceil($count/$size);if($pages>2000){throw new Exception('Unexpected gallery size.');}for($p=2;$p<=$pages;$p++){$job['queue'][]=array($id,$p);}}
  if($job['groups'][$id]['sourceCount']!==$count){throw new Exception('The source changed during refresh. Please try again.');}
  $fingerprint=$id.':'.hash('sha256',wp_json_encode(array_column($gallery['shows'],'showId')));
  if(isset($job['seen'][$fingerprint])){throw new Exception('CCTV returned a duplicate page.');}$job['seen'][$fingerprint]=true;
  $job['received'][$id]=($job['received'][$id]??0)+count($gallery['shows']);
  foreach($gallery['shows'] as $s){if(empty($s['vodUrl'])){continue;}$sid=(int)$s['showId'];$row=$job['rows'][$sid]??array($sid,(string)$s['title'],empty($s['thumbnailUrl'])?null:basename($s['thumbnailUrl']),array(),array());$row[3]=array_values(array_unique(array_merge($row[3],array($id))));$row[4]=array_values(array_unique(array_merge($row[4],array($g['channel']))));$job['rows'][$sid]=$row;}
  if(!$job['queue']){
   foreach($job['groups'] as $g){if(($job['received'][$g['id']]??0)!==$g['sourceCount']){throw new Exception('Incomplete gallery.');}}
   if(count($job['rows'])<count(cctv_dir_catalog()['rows'])*0.8){throw new Exception('The source returned far fewer videos than expected. Previous directory retained.');}
   $job['phase']='navigator-index';
  }
 } elseif($job['phase']==='navigator-index') {
  $html=cctv_dir_http(CCTV_DIR_NAV);preg_match_all('/href=["\']([^"\']+)["\']/i',$html,$m);$pages=array();
  foreach($m[1] as $href){$href=explode('#',html_entity_decode($href,ENT_QUOTES,'UTF-8'))[0];if(strpos($href,'://')!==false||strpos($href,'//')===0||strpos($href,'..')!==false||strpos($href,'DataQualityReport')!==false||!preg_match('/\.html$/i',$href)){continue;}$pages[CCTV_DIR_NAV.ltrim($href,'/')]=true;}
  if(!$pages){throw new Exception('The meeting navigator returned no pages.');}$job['queue']=array_keys($pages);$job['phase']='navigator';
 } elseif($job['phase']==='navigator') {
  $url=array_shift($job['queue']);$ids=cctv_dir_primary_ids(cctv_dir_http($url));if(count($ids)===1){$job['links'][$ids[0]][]=$url;}
  if(!$job['queue']){$job['phase']='publish';}
 } elseif($job['phase']==='publish') {
  $rows=array_values($job['rows']);usort($rows,function($a,$b){return $b[0]<=>$a[0];});foreach($rows as &$row){$row[5]=$job['links'][$row[0]]??array();}unset($row);
  $catalog=array('updated'=>gmdate('c'),'categories'=>array_values($job['groups']),'rows'=>$rows,'version'=>substr(hash('sha256',wp_json_encode($rows)),0,16));
  if(!update_option('cctv_dir_catalog',$catalog,false)){throw new Exception('Could not save the refreshed directory.');}
  update_option('cctv_dir_status',array('running'=>false,'message'=>'Updated '.number_format(count($rows)).' videos and meeting links.','at'=>time()),false);delete_option('cctv_dir_job');return;
 }
 $job['done']++;update_option('cctv_dir_job',$job,false);update_option('cctv_dir_status',array('running'=>true,'message'=>'Refreshing: '.$job['done'].' source pages processed. Current directory remains available.','at'=>time()),false);
 }catch(Exception $e){delete_option('cctv_dir_job');update_option('cctv_dir_status',array('running'=>false,'message'=>'Refresh stopped: '.$e->getMessage(),'at'=>time()),false);}
 finally{delete_option('cctv_dir_lock');if(get_option('cctv_dir_job')&&!wp_next_scheduled('cctv_dir_step')){wp_schedule_single_event(time()+5,'cctv_dir_step');}}
}
function cctv_dir_manifest(){nocache_headers();$c=cctv_dir_catalog();wp_send_json(array('version'=>$c['version'],'updated'=>$c['updated'],'count'=>count($c['rows']),'file'=>'catalog.'.$c['version'].'.json'));}
function cctv_dir_download(){nocache_headers();$c=cctv_dir_catalog();$v=isset($_GET['version'])?sanitize_text_field(wp_unslash($_GET['version'])):'';if($v!==$c['version']){wp_send_json(array('error'=>'Catalog changed. Please try again.'),409);}wp_send_json($c);}
function cctv_dir_view(){
 nocache_headers();header('Content-Type: text/html; charset='.get_bloginfo('charset'));$html=file_get_contents(__DIR__.'/assets/index.html');$c=cctv_dir_catalog();
 $html=preg_replace_callback('~<script id="catalog-data" type="application/json">.*?</script>~s',function()use($c){return '<script id="catalog-data" type="application/json">'.wp_json_encode($c,JSON_HEX_TAG|JSON_HEX_AMP|JSON_HEX_APOS|JSON_HEX_QUOT).'</script>';},$html);
 $config=array('manifest'=>admin_url('admin-ajax.php?action=cctv_directory_manifest'),'catalog'=>admin_url('admin-ajax.php?action=cctv_directory_catalog'),'view'=>admin_url('admin-ajax.php?action=cctv_directory_view'));
 $html=str_replace('</head>','<script>window.CCTV_WP='.wp_json_encode($config,JSON_HEX_TAG|JSON_HEX_AMP|JSON_HEX_APOS|JSON_HEX_QUOT).';</script></head>',$html);
 $html=str_replace('href="./"','href="'.esc_url($config['view']).'"',$html);echo $html;exit;
}
foreach(array('view','manifest','catalog') as $route){$fn=$route==='catalog'?'cctv_dir_download':'cctv_dir_'.$route;add_action('wp_ajax_cctv_directory_'.$route,$fn);add_action('wp_ajax_nopriv_cctv_directory_'.$route,$fn);}
add_shortcode('cctv_directory',function(){wp_enqueue_script('cctv-directory-frame',plugins_url('assets/frame.js',__FILE__),array(),'1.0.0',true);return '<iframe class="cctv-directory-frame" title="CCTV Video Library" src="'.esc_url(admin_url('admin-ajax.php?action=cctv_directory_view')).'" style="width:100%;min-height:600px;border:0;display:block" loading="eager"></iframe>';});
add_action('admin_menu',function(){add_options_page('CCTV Directory','CCTV Directory','manage_options','cctv-directory','cctv_dir_settings');});
function cctv_dir_settings(){if(!current_user_can('manage_options')){return;}wp_enqueue_script('cctv-directory-admin',plugins_url('assets/admin.js',__FILE__),array(),'1.0.0',true);wp_localize_script('cctv-directory-admin','CCTV_ADMIN',array('url'=>admin_url('admin-ajax.php'),'nonce'=>wp_create_nonce('cctv_directory_admin')));$c=cctv_dir_catalog();$status=get_option('cctv_dir_status');echo '<div class="wrap"><h1>CCTV Video Directory</h1><p>Add a Shortcode block to any page and enter <code>[cctv_directory]</code>.</p><p>Available now: '.esc_html(number_format(count($c['rows']))).' videos. Directory date: '.esc_html($c['updated']).'.</p><p>Refresh retrieves the full CCTV directory and matching school board meeting pages. The existing directory stays available until a complete refresh succeeds.</p><p><button class="button button-primary" id="cctv-refresh">Refresh from CCTV</button></p><p id="cctv-admin-status" role="status">'.esc_html($status['message']??'Ready.').'</p><p>Updates also run daily through WordPress scheduled tasks. Keeping this page open during a manual refresh helps it finish faster. On low-traffic sites, your host can configure a regular WordPress cron run.</p></div>';}
add_action('wp_ajax_cctv_directory_admin',function(){check_ajax_referer('cctv_directory_admin','nonce');if(!current_user_can('manage_options')){wp_send_json_error('Administrator access required.',403);}if(isset($_POST['start'])){cctv_dir_start();}cctv_dir_step();wp_send_json_success(get_option('cctv_dir_status',array('running'=>false,'message'=>'Ready.')));});
