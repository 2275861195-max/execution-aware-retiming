import fs from 'node:fs/promises';
import path from 'node:path';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
import { pathToFileURL } from 'node:url';

const skill = process.env.PRESENTATION_SKILL_DIR;
if (!skill || !process.env.RUNTIME_PYTHON) throw new Error('Set PRESENTATION_SKILL_DIR and RUNTIME_PYTHON to the bundled presentation runtime');
const { finalizePresentation, resolvePresentationFont, applyPresentationChartFont } = await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')));

const workspaceDir = path.dirname(new URL(import.meta.url).pathname);
const build = path.join(workspaceDir, '.build');
await fs.mkdir(build, { recursive: true });
await fs.mkdir(path.join(workspaceDir,'output'), {recursive:true});
const font = resolvePresentationFont({ fontFamily: 'Arial' });
const p = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const ink = '#1D2935', teal = '#136F73', coral = '#B94C3D', grey = '#536575';
const source = 'Source: author-supplied research meeting brief, 12 October 2026. Aggregate observations and exploratory associations are separate evidence tiers.';
function text(s, value, x, y, w, h, size = 28, color = ink, bold = false) {
  const sh = s.shapes.add({ geometry: 'textbox', position: { left:x, top:y, width:w, height:h }, fill:'none', line:{fill:'none',width:0} });
  sh.text = value;
  sh.text.style = {typeface:font,fontSize:size,color,bold};
  return sh;
}
function slide(title, notes) {
  const s=p.slides.add(); s.background.fill='#FAFBFA';
  text(s,title,64,44,1152,96,43,ink,true);
  s.speakerNotes.text=source+'\n'+notes;
  return s;
}
function box(s,label,x,y,w=210,h=110,color=teal) {
  const b=s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill:'#FFFFFF',line:{fill:color,width:2}});
  b.text=label; b.text.style={typeface:font,fontSize:26,color:ink,alignment:'center'};return b;
}
function link(s,a,b,opts={}) {return s.shapes.connect(a,b,{kind:'straight',fromSide:'right',toSide:'left',line:{fill:grey,width:2},tail:{type:'arrow'},...opts});}
function chart(s,type,config) {
 const c=s.charts.add(type,config);applyPresentationChartFont(c,{fontFamily:font});
 for(const axis of [c.xAxis,c.yAxis]){axis.textStyle.fontSize=20;axis.title.textStyle.fontSize=20;}
 c.dataLabels.textStyle.fontSize=20;
 return c;
}

{
 const s=slide('Towards Stable Temporal Acceleration\nof Frozen Action-Chunk Policies','Tentative project title. This meeting concerns mechanism identification, not a completed method. We seek feedback and collaborators.');
 text(s,'Current empirical evidence and mechanism-identification plan',64,275,1100,100,32,grey);
 text(s,'Research discussion · 13 October 2026',64,480,1050,50,26,teal);
 text(s,'Stability plug-in: a research target, not a validated method',64,565,1100,70,25,coral);
}
{
 const s=slide('Deployment-time acceleration','The policy is frozen. Temporal acceleration is an execution intervention. The accelerator itself is not necessarily our contribution. Reliability and measured speedup must both improve.');
 text(s,'Can frozen policies execute faster\nwithout losing reliability?',64,170,1110,140,45,ink,true);
 text(s,'Existing accelerator\nShortens execution of a predicted action chunk',64,360,535,140,30,teal);
 text(s,'Research target\nMinimal execution correction after acceleration',680,360,535,140,30,teal);
 text(s,'Evaluation requires actual speed gain, success rate, and execution traces.',64,590,1140,80,27,grey);
}
{
 const s=slide('Current execution pipeline','The existing experiments use frozen π0.5 and a 10-action chunk. Runtime retiming acts on execution. Policy independence and ACT/DP generalization remain future tests. Query cadence changes with acceleration in the current protocols.');
 const labels=['Observation','Frozen π0.5','10-action\nchunk','Runtime\nretime','Execution'];
 const bs=labels.map((l,i)=>box(s,l,64+i*238,250,202,120));for(let i=0;i<4;i++)link(s,bs[i],bs[i+1]);
 text(s,'No policy fine-tuning in this comparison',64,450,1135,55,31,teal);
 text(s,'Current protocols also change when the policy is queried.',64,540,1135,80,29,coral);
}
{
 const s=slide('Reliability falls while measured speed gain saturates','Verified supplied overall table: RT1 SR97.90,time7.43,speedup1.00,calls15.29; RT1.5 95.45,5.76,1.33,19.61; RT2 80.50,5.57,1.47,22.71; RT2.5 60.70,5.73,1.54,29.04; RT3 48.85,5.55,1.53,37.34. Completion-time and call means condition on success. Exact paired denominator needs documentation. No confidence intervals have been supplied.');
 chart(s,'line',{position:{left:55,top:160,width:710,height:390},categories:['1.0×','1.5×','2.0×','2.5×','3.0×'],series:[{name:'Success rate (%)',values:[97.9,95.45,80.5,60.7,48.85],line:{fill:teal,width:3},marker:{symbol:'circle',size:9,fill:teal}}],hasLegend:false,dataLabels:{showValue:true,position:'top',numberFormatCode:'0.00'},yAxis:{minimumScale:0,maximumScale:100,numberFormatCode:'0',title:'Success rate (%)'},xAxis:{title:'Requested acceleration'}});
 text(s,'1.5× requested\n95.45% success\n1.33× paired speedup',830,190,360,165,30,teal,true);
 text(s,'3.0× requested\n48.85% success\n1.53× paired speedup',830,390,360,165,30,coral,true);
 text(s,'Supplied aggregate results. Paired speedup is distinct from requested acceleration.\nSuccessful-episode metrics and paired eligibility require explicit denominators.',64,606,1152,78,21,grey);
}
{
 const s=slide('Exploratory RT3 diagnostic associations','The 100-episode audit contains an RT3 subset with 31 failures and 19 successes. These are medians over first100 control steps,5seconds. Three proxies have different units and should not be interpreted on a common scale. Bound excess is requested action excess, not verified physical saturation. Task4 direction reverses:failure.1793,success.2386. Task8 efficiency reverses:failure.8551,success.8329. No causal order or universal signal established.');
 const table=s.tables.add({rows:4,columns:3,left:64,top:145,width:1152,height:350,columnWidths:[670,241,241],values:[['Median proxy','Failure N=31','Success N=19'],['Direction-change proxy','0.1793','0.1061'],['Requested bound-excess fraction','0.64','0.63'],['EEF path efficiency','0.7469','0.8368']]});
 table.borders.assign({fill:'#D6E0E0',width:1});
 for(let r=0;r<4;r++)for(let c=0;c<3;c++){const cell=table.getCell(r,c);cell.fill=r===0?'#EAF1F0':'#FAFBFA';cell.text.style={typeface:font,fontSize:27,color:c===1?coral:c===2?teal:ink,bold:r===0};}
 text(s,'First 100 control steps = 5 seconds for each episode',64,535,1140,50,25,grey);
 text(s,'Association only. Task-level counterexamples exist.\nNo validated universal instability signal.',64,600,1140,80,27,coral,true);
}
{
 const s=slide('Four competing mechanism hypotheses','These are competing hypotheses, not a ranked explanation. They may coexist. Object/contact/task-predicate signals are missing from the old diagnostic traces, preventing current adjudication.');
 const hs=[['H1','Motion realization distortion','Requested motion differs from realized execution'],['H2','Cross-query commitment instability','Replanning changes continuous or discrete intent'],['H3','Interaction completion mismatch','Actuation advances before grasp or placement settles'],['H4','Object-state deviation / failed recovery','Object perturbation leads to inconsistent recovery']];
 hs.forEach((h,i)=>{const y=160+i*116;text(s,h[0],64,y,90,50,35,teal,true);text(s,h[1],165,y,1040,50,31,ink,true);text(s,h[2],165,y+48,1040,48,25,grey);});
 text(s,'No winner yet',64,645,1100,45,25,coral);
}
{
 const s=slide('Acceleration and query cadence are confounded','RT1 executes 10 raw actions before querying. RT3 executes 3 compressed actions before querying. Therefore both source-time compression and cadence/prefix execution differ. Existing RT1 versus RT3 comparisons cannot identify either factor independently.');
 const a=box(s,'RT1\nSpeed 1×\nQuery every 10 steps',120,210,430,190);
 const b=box(s,'RT3\nSpeed 3×\nQuery every 3 steps',730,210,430,190,coral);link(s,a,b);
 text(s,'Speed changes',145,460,450,55,33,coral,true);text(s,'Query cadence changes',725,460,490,55,33,coral,true);
 text(s,'The current comparison cannot separate these effects.',64,585,1150,80,33,ink,true);
}
{
 const s=slide('Controlled protocol comparison','Proposed design, not completed results. Task4 is falsification oriented because the direction proxy has a task-level counterexample. 20 fixed outcome-independent init states. Brief proposes 6 smoke then60 diagnostic episodes with possible repeats. Latest collection plan may use100 including Q3 repeats. S1Q10 toS1Q3 tests cadence plus chunk-prefix execution and feedback opportunity changes. S1Q3 toS3Q3 matches cadence but changes temporal compression and source coverage.');
 const a=box(s,'S1-Q10\nRaw 10 steps',90,185,295,125);
 const b=box(s,'S1-Q3\nRaw a0, a1, a2',875,185,295,125);
 const c=box(s,'S3-Q3\n3 compressed steps',490,410,295,125,coral);
 link(s,a,b);link(s,b,c,{fromSide:'bottom',toSide:'right'});link(s,a,c,{fromSide:'bottom',toSide:'left',line:{fill:'#ACB6BB',width:1,style:'dashed'}});
 text(s,'Cadence / prefix-execution effects',412,195,450,70,26,teal);
 text(s,'Compression at\nmatched cadence',865,400,325,80,26,coral);
 text(s,'Task4: a counterexample test\n20 fixed, outcome-independent init states',64,586,1150,88,28,grey);
}
{
 const s=slide('Synchronized execution diagnostics','Required new logging:task,init,repeat,seed,step,simtime,query/localindex;raw/retimedchunk,sourcemapping,actionsent;actualscaleddelta/controllergoalsifaccessible;EEF/robot/gripperpositionsandvelocities;allmovableobjectpose/velocity;finger/robot/support/receptaclecontacts;predicates/reward/done/finalsuccess. Agentview andwrist video map explicitly to steps. Privileged state diagnoses mechanisms but does not define deployable plugin inputs.');
 const labels=['Action\nsource mapping','Controller\nphysical goal','Robot\nEEF / gripper','Object\npose / contact','Predicate\ntask progress'];
 const bs=labels.map((l,i)=>box(s,l,64+i*238,230,202,130));for(let i=0;i<4;i++)link(s,bs[i],bs[i+1]);
 text(s,'Shared identity: init, repeat, seed, query, control step, simulation time',64,445,1150,90,29,teal);
 text(s,'Agentview + wrist video synchronized to control steps',64,545,1150,55,28);
 text(s,'Simulator ground truth supports diagnosis. Deployment inputs remain open.',64,625,1150,60,23,coral);
}
{
 const s=slide('Future stability plug-in and meeting questions','Architecture is conceptual and not implemented. Monitor and corrector depend on the identified mechanism. Possible corrections include feasibility/residual handling,commitment filtering,completion-awareexecution,or conservative recovery. No effect demonstrated. Questions:is the problem focused;does S1Q3 control adequately separate cadence;what deployable signal should be targeted?');
 const a=box(s,'Existing\naccelerator',80,170,280,100),b=box(s,'Proposed stability plug-in\nMonitor + Corrector',490,170,400,100,coral),c=box(s,'Robot',1010,170,185,100);link(s,a,b);link(s,b,c);
 link(s,c,b,{fromSide:'bottom',toSide:'bottom',kind:'elbow',line:{fill:grey,width:2,style:'dashed'}});
 text(s,'Mechanism-dependent and under investigation',490,300,700,50,24,coral);
 text(s,'1  Is execution instability a sufficiently focused research problem?',64,397,1152,65,28);
 text(s,'2  What remains confounded in the S1-Q3 control?',64,478,1152,65,28);
 text(s,'3  Which deployment signal can support minimal correction?',64,559,1152,65,28);
 text(s,'Seeking collaborators in execution diagnostics and controlled robot experiments',64,655,1152,38,20,teal);
}
await (await PresentationFile.exportPptx(p)).save(path.join(build,'candidate.pptx'));
for(let i=0;i<p.slides.items.length;i++)await fs.writeFile(path.join(build,`slide-${i+1}.png`),new Uint8Array(await (await p.export({slide:p.slides.items[i],format:'png',scale:1})).arrayBuffer()));
const result=await finalizePresentation({workspaceDir,candidatePath:path.join(build,'candidate.pptx'),finalPath:path.join(workspaceDir,'output','meeting_slides.pptx'),pythonExecutable:process.env.RUNTIME_PYTHON,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit','--require-native-table-slide','5'],explicitTotalSlideCount:10,requiredNativeChartOwnerSlides:[4],requiredNativeTableOwnerSlides:[5],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:path.join(build,'validation.json')});
await fs.copyFile(path.join(workspaceDir,'output','meeting_slides.pptx'),path.join(workspaceDir,'meeting_slides.pptx'));
console.log(result);
