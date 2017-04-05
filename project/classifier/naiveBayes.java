/******************************************************************************
 * naiveBayes.java
 * SENG 474 - Data Mining Project
 * This program is an implementation of the Naive Bayes multinomial algorithm.
 * It is intended for use on news articles, with the primary purpose being
 * to differentiate between "fake" news articles and "real" news articles.
 *
 * Input files are passed in through command line.
 ******************************************************************************/
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.io.File;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Map;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.FileReader;
import java.util.Arrays;

import com.opencsv.CSVReader;
import org.apache.commons.lang3.StringUtils;

public class naiveBayes {

	public static List<String> vocabulary = new ArrayList<String>();
	public static List<Document> documents = new ArrayList<Document>();
	public static List<Document> trainingDocuments = new ArrayList<Document>();
	public static List<Document> testingDocuments = new ArrayList<Document>();

	public static List<ClassLabel> classLabels = new ArrayList<ClassLabel>();
	public static int trueDocuments = 0;
	public static int falseDocuments = 0;
	public static final int threshold = 200;

	/****************************************************************************
	 * getNews()
	 * Creates list of document objects from news.csv
	 * todo: change to passed in file
	 ****************************************************************************/
	public static void getNews(String inputfile) {
		try {
			//CSVReader reader = new CSVReader(new FileReader("news.csv"), ',' , '"' , 1);
			CSVReader reader = new CSVReader(new FileReader(inputfile), ',' , '"' , 1);
			String[] nextLine;
			int i = 0;
			while ((nextLine = reader.readNext()) != null) {
        i++;
				if (nextLine.length == 5) {
					if (nextLine[4].equals("1")) {
						documents.add(new Document(nextLine[0], nextLine[1], nextLine[2], nextLine[3], true));
					} else {
						documents.add(new Document(nextLine[0], nextLine[1], nextLine[2], nextLine[3], false));
					}
				}
			}
			reader.close();
		} catch(Exception e) {
			System.out.println(e);
			System.out.println("Verify " + inputfile + " is in the right location.");
			return;
		}

	}
	/****************************************************************************
	 * divideDocuments()
	 * Divides documents into trainingDocuments and testingDocuments
	 * loop through document list and for every nth document we encounter
	 * throw it into a training set.
	 * We do this until we hit our hardcoded threshold for the number
	 * of training documents we want.
	 * All other documents go into the testing set.
	 ****************************************************************************/
	public static void divideDocuments() {

		int rand = (int)(Math.random() * 4 + 1);
		int training_true = 0;
		int training_false = 0;

		for (int i = 0; i < documents.size(); i++) {
			if( training_true < threshold && i % rand == 0 && documents.get(i).getLabel() == true ) {
				trainingDocuments.add(documents.get(i));
				training_true++;
			}
			else if (training_false < threshold
			         && i % rand == 0
							 && documents.get(i).getLabel() == false) {
				trainingDocuments.add(documents.get(i));
				training_false++;
			}
			else {
				testingDocuments.add(documents.get(i));
			}
		}

	}
	/****************************************************************************
	 * createVocabulary()
	 * Creates dictionary by scanning document objects
	 ****************************************************************************/
	public static void createVocabulary() {
		for (int i = 0; i < trainingDocuments.size(); i++) {

			Scanner document = new Scanner(trainingDocuments.get(i).getText());
			while (document.hasNextLine()) {

				Scanner line = new Scanner(document.nextLine());
				while (line.hasNext()) {

					String term = line.next();
					term = term.toLowerCase();
					term = term.replaceAll("[^a-z]", "");
					boolean present = false;
					for (int j = 0; j < vocabulary.size(); j++) {

						if (vocabulary.get(j).equals(term)) {
							present = true;
							break;
						}
					}
					if (!present) {
						vocabulary.add(term);
					}
				}
			}
		}
		System.out.println("# of terms in vocabulary: " + vocabulary.size());
	}
	/****************************************************************************
	 * configure()
	 * Adds a true and false class label to classLabels
	 ****************************************************************************/
	public static void configure() {
		classLabels.add(new ClassLabel(true, ((float)threshold / trainingDocuments.size())));
		classLabels.add(new ClassLabel(false, ((float)threshold / trainingDocuments.size())));
	}
	/****************************************************************************
	 * vocabulary()
	 * Iterates through vocabulary and sums the amount of times each term appears
	 ****************************************************************************/
	public static void vocabulary(List<String> terms, int index) {

		int distinctTerms = 0;
		for (int i = 0; i < vocabulary.size(); i++) {

			String term  = vocabulary.get(i);
			for (int j = 0; j < terms.size(); j++) {

				if (terms.get(j).equals(term)) {
					distinctTerms++;
					break;
				}
			}
		}

		for (int i = 0; i < vocabulary.size(); i++) {

			String term  = vocabulary.get(i);
			int termAppearences = 0;
			for (int j = 0; j < terms.size(); j++) {

				if (terms.get(j).equals(term)) {
					termAppearences++;
				}
			}
			classLabels.get(index).probability.put(term, ((float)(termAppearences + 1.00) / (distinctTerms + vocabulary.size())));
		}
	}
	/****************************************************************************
	 * calculateProbability()
	 * Calculates probability of terms appearing in trainingDocuments
	 ****************************************************************************/
	public static void calculateProbability() {
		for (int i = 0; i < classLabels.size(); i++) {
			List<String> terms = new ArrayList<String>();

			for (int j = 0; j < trainingDocuments.size(); j++) {

				if (trainingDocuments.get(j).getLabel() == classLabels.get(i).getLabel()) {
					Scanner document = new Scanner(trainingDocuments.get(j).getText());
					while (document.hasNextLine()) {

						Scanner line = new Scanner(document.nextLine());
						while (line.hasNext()) {

							String term  = line.next();
							term = term.toLowerCase();
							term = term.replaceAll("[^a-z]", "");
							terms.add(term);
						}
					}
				}
			}
			vocabulary(terms, i);
		}
	}
	/****************************************************************************
	 * printProbability()
	 * Prints probabilities
	 * Was used for testing. Method currently not in use.
	 ****************************************************************************/
	public static void printProbability() {
		for (int i = 0; i < classLabels.size(); i++) {

			for (int j = 0; j < vocabulary.size(); j++) {

				String term  = vocabulary.get(j);
				System.out.println("Class: " + classLabels.get(i).getLabel() + " |  Term: " + term + " |  Probability: " + classLabels.get(i).probability.get(term));
			}
		}
	}
	/****************************************************************************
	 * trainClassifier()
	 * Training phase of the Naive Bayes classifier.
	 * This phase is subdivided into 5 main parts:
	 *     getNews - read in tuples from our data set.
	 *     divide -
	 *     createVocabulary
	 *     configure
	 *     calculateProbability
	 ****************************************************************************/
	public static void trainClassifier(String inputfile) {
		getNews(inputfile);
		divideDocuments();
		createVocabulary();
		configure();
		calculateProbability();
	}
	/****************************************************************************
	 * testClassifier()
	 * Testing phase of the classifier.
	 * No explicit input given to this procedure but it implicitly
	 * runs through all remaining articles in our Document set.
	 * For each article, it:
	 * - calculates the probability article is real or fake
	 * - takes the higher probability of the two guesses
	 * - compares guess to its actual class value
	 * - uses comparison result to place guess into confusion matrix
	 ****************************************************************************/
	public static void testClassifier() {
		int truePositive = 0;
		int falsePositive = 0;
		int trueNegative = 0;
		int falseNegative = 0;

		for (int k = 0; k < testingDocuments.size(); k++) {

			List<String> terms = new ArrayList<String>();
			Map<Boolean, Double> score = new HashMap<Boolean, Double>();
			Scanner document = new Scanner(testingDocuments.get(k).getText());

			while (document.hasNextLine()) {
				Scanner line = new Scanner(document.nextLine());

				while (line.hasNext()) {

					String term = line.next();
					term = term.toLowerCase();
					term = term.replaceAll("[^a-z]", "");

					for (int j = 0; j < vocabulary.size(); j++) {
						if (vocabulary.get(j).equals(term)) {
							terms.add(term);
							break;
						}
					}
				}
			}

			for (int i = 0; i < classLabels.size(); i++) {

				score.put(classLabels.get(i).getLabel(), Math.log(classLabels.get(i).getRatio()));
				for (int j = 0; j < terms.size(); j++) {

					score.put(classLabels.get(i).getLabel(), score.get(classLabels.get(i).getLabel()) + Math.log(classLabels.get(i).probability.get(terms.get(j))));
				}
			}

			double trueScore = score.get(true);
			double falseScore = score.get(false);

			if (trueScore > falseScore) {
				if (testingDocuments.get(k).getLabel()) {
					truePositive++;
				} else {
					falsePositive++;
				}
			} else {
				if (!testingDocuments.get(k).getLabel()) {
					trueNegative++;
				} else {
					falseNegative++;
				}
			}
		}
		System.out.println("TP | FP | TN | FN");
		System.out.println(truePositive + " | "
		                   + falsePositive + " | "
											 + trueNegative + " | "
											 + falseNegative );
	}
	/****************************************************************************
	 *                  P R O G R A M    S T A R T S    H E R E
	 ****************************************************************************/
	public static void main(String[] args) {
		// verify we have the right # of arguments
		if (args.length == 0) {
			System.out.println("Usage of program:");
			System.out.println("java -cp .;opencsv-3.9.jar;commons-lang3-3.5.jar naiveBayes input.csv");
			return;
		}
		// verify input file path exists
		trainClassifier(args[0]);
		testClassifier();
	}

}
/******************************************************************************
 * Class definition for our news documents.
 * Each news document from our input CSVs contains the following attributes:
 * - a unique sha1 hash used as an identifier
 * - the title of the article
 * - the article text
 * - the domain from which we fetched the article
 * - the class label we've associated with our document
 * Currently, documents can be "real" or "fake" news.
 ******************************************************************************/
class Document {

	private String uuid;
	private String title;
	private String text;
	private String domain;
	private boolean label;

	public Document(String uuid, String title, String text, String domain, boolean label) {
		this.uuid = uuid;
	  this.title = title;
	  this.text = text;
	  this.domain = domain;
		this.label = label;
	}

	public boolean getLabel() {
		return label;
	}

	public String getText() {
		return text;
	}

	public String getDomain() {
		return domain;
	}
}
/******************************************************************************
 * Class defintion for our document classifications.
 * The important thing here is that each classification has a probability
 * associated with it. These probabilities are computed during the training
 * phase of classification and are referenced when testing on incoming articles.
 ******************************************************************************/
class ClassLabel {

	private boolean label;
	private float ratio;
	public Map<String, Float> probability = new HashMap<String, Float>();

	public ClassLabel(boolean label, float ratio) {
		this.label = label;
		this.ratio = ratio;
	}

	public boolean getLabel() {
		return label;
	}

	public float getRatio() {
		return ratio;
	}
}
