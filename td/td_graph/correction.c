#include <stdio.h>
#include <stdlib.h>
#include <time.h>


typedef struct { //graphe représenté par une matrice d'adjacence
  	int nombre_sommet;
  	int ** matrice_adjacence;
} graphe;


void affiche_graphe(graphe G){
	int i,j;
	printf("Graphe avec %d sommets \n",G.nombre_sommet);
	for(i = 0; i<G.nombre_sommet; i++){
		printf("Voisins de %d: ",i);
		for(j = 0; j < G.nombre_sommet; j++){
			if(G.matrice_adjacence[i][j]) printf("%d ",j);
		}
		printf("\n");
	}
}

//Crée le fichier "graphX.pdf" (X = str en param)
//Le fichier n'est généré que si la fonction init_graph est implémentée
void ecrire_fichier_dot(graphe G,char* str){
	if(G.matrice_adjacence == NULL)return;
	FILE* f;
	char buf[64];
	sprintf(buf,"graph%s.dot",str);
	if( !(f = fopen(buf,"w")) ){
		perror("Opening dot file failure\n");exit(2);
	}
	fprintf(f,"graph G { \n");
	for(int i=0;i<G.nombre_sommet;i++){fprintf(f,"%d \n",i);}
	for(int i=0;i<G.nombre_sommet;i++){
		for(int j=0;j<i;j++){
			if(G.matrice_adjacence[i][j]){
				fprintf(f,"%d -- %d\n",i,j);
			}
		}
	}
	fprintf(f,"} \n");
	fclose(f);
	sprintf(buf,"neato -Tpdf graph%s.dot -o graph%s.pdf",str,str);
	system(buf);

}

int degre(graphe G, int i){
	return 0;
}


graphe init_graphe(int n){//créé un graphe dont tous les sommets sont isolés
	graphe G; 
	G.nombre_sommet = n;
	G.matrice_adjacence = malloc(sizeof(int*)*n);
	for(int i=0;i<G.nombre_sommet;i++)
	{
		G.matrice_adjacence[i] = calloc(n,sizeof(int));
	}
	return G;
}

void libere_graphe(graphe G){
	for(int i=0;i<G.nombre_sommet;i++)
	{
		free(G.matrice_adjacence[i]);
		
	}

	free(G.matrice_adjacence);
}

graphe cycle_graphe(int n){//créé un cycle
	graphe G = init_graphe(n);
	for(int i=0;i<G.nombre_sommet;i++){
		G.matrice_adjacence[i][(i-1 + n) % n] = 1;
		G.matrice_adjacence[i][(i+1) % n] = 1;
		
	}
	return G;
}


graphe complet_graphe(int n){//créé un graphe complet
	graphe G=init_graphe(n);
	for(int i=0;i<G.nombre_sommet;i++)
	{
		for(int j=0;j<G.nombre_sommet;j++)
			if(i != j)
				G.matrice_adjacence[i][j] =1;
	}
	return G;
}

float rand01()
{
	return (float)rand() / (float)RAND_MAX;
} 

graphe alea_graphe(int n, float p){
	graphe G=init_graphe(n);
	for(int i=0;i<G.nombre_sommet;i++)
	{
		for(int j=0;j<i;j++)
			if(i != j){
				if(rand01()<p)
				{
					G.matrice_adjacence[i][j] =1;
					G.matrice_adjacence[j][i] =1;
				}
			}

	}
	return G;
}

graphe graphe_arbre(int *pere, int n){//créer un arbre couvrant à partir du tableau des pères représenté comme un graphe
	graphe G=init_graphe(n);

	for(int i=0;i<G.nombre_sommet;i++)
	{
		if(pere[i] != i)
		{
			G.matrice_adjacence[i][pere[i]] = 1;
			G.matrice_adjacence[pere[i]][i] = 1;
		}
	}

	return G;
}

void parcours_sommet(graphe G, int s, int *couleur, int *pere){
	couleur[s] = 1;
	for(int i=0;i<G.nombre_sommet;i++)//Pour tout les sommets 
	{
		if(G.matrice_adjacence[s][i])//Si l'arrete existe (c'est mon voisin)
		{
			if(couleur[i] == 0)//Si le sommet n'a jamais été visité
			{
				pere[i] = s;
				
				parcours_sommet(G,i,couleur,pere);
				
			}
		}
	}
	couleur[s]=2; //on remonte
	printf("%d ",s);
	
}

graphe parcours_graphe(graphe G){
	int *couleur = calloc(G.nombre_sommet,sizeof(int)); // 0 est blanc, 1 gris et 2 noir
	int *pere = malloc(sizeof(int)*G.nombre_sommet);
	int composante = 0;

	for(int i=0;i<G.nombre_sommet;i++){ //init
		couleur[i]=0;
		pere[i]=i;
	}

	for(int i=0;i<G.nombre_sommet;i++){
		if(couleur[i] == 0)
		{
			printf("Nouvelle composante ! %d : \n",composante);composante++;
			parcours_sommet(G,i,couleur,pere);
			printf("\n");
			
		}
	}
	graphe res = graphe_arbre(pere,G.nombre_sommet);
	

	free(couleur);
	free(pere);
	return res;
}


  
void cycle_eulerien(graphe G){//on suppose le graphe connexe
}


int main(){
	/* Tests pour vérifier si vos implémentations sont correctes*/
	srand(time(NULL));
  	graphe G = cycle_graphe(10);
  	affiche_graphe(G);
  	ecrire_fichier_dot(G,"Cycle");
	graphe H = complet_graphe(5);
	affiche_graphe(H);
	ecrire_fichier_dot(H,"Complet");
	graphe L = alea_graphe(10,0.2);
	affiche_graphe(L);
	ecrire_fichier_dot(L,"Alea");
	graphe A = parcours_graphe(L);
	affiche_graphe(A);
	ecrire_fichier_dot(A,"Arbre");
	cycle_eulerien(L);
	cycle_eulerien(H);
	libere_graphe(G);
	libere_graphe(H);
	libere_graphe(L);
	libere_graphe(A);
}
