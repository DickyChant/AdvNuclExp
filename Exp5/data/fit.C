double ch2time(int ch){
	return ch * 0.0265 + 9.2530;
}
void fit(){
	auto gr = new TGraph();
	ifstream txtin;
	txtin.open("5ks.txt");
	int count = 0;
	for(int i = 0; i < 1024; i++){
		
		txtin >> count;
		gr->SetPoint(i,ch2time(i+1),count);
	}

	
	auto fout = new TFile("test.root","recreate");
	auto f1 = new TF1("f1","[0]*exp(-[1]*x)",18,21);
	gr->Fit("f1","R");
	gr->Write("tg5ks");
	f1->Write();
	auto gr1 = new TGraph();
	auto counts = gr->GetY();
	auto dts = gr->GetX();
	for(int i = 0; i < 1024; i++){
		
		gr1->SetPoint(i,ch2time(i+1),counts[i]-f1->Eval(ch2time(i+1)));
	}
	auto f2 = new TF1("f2","[0]*exp(-[1]*x)",16.4,17.4);
	f2->SetParameters(3.35274E12,2.51385);
	gr1->Fit("f2","R");
	f2->Write();
    gr1->Write("tg5ksprime");
	gr1->Draw();
	
	fout->Close();

}
