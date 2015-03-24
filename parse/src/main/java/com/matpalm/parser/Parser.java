package com.matpalm.parser;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.Properties;

import edu.stanford.nlp.ling.CoreAnnotations.LemmaAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.PartOfSpeechAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;

public class Parser {
  public static void main(String[] s) throws Exception {

    Reader reader;
    if (System.getProperty("IN") == null) {
      reader = new InputStreamReader(System.in);
    } else {
      reader = new FileReader(System.getProperty("IN"));
    }
    BufferedReader input = new BufferedReader(reader);

    Properties props = new Properties();
    props.setProperty("annotators", "tokenize, ssplit, pos, lemma");
    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

    String text;
    while ((text = input.readLine()) != null) {
      try {
        Annotation document = new Annotation(text);
        pipeline.annotate(document);

        StringBuilder output = new StringBuilder();
        boolean firstToken = true;
        for (CoreMap sentence: document.get(SentencesAnnotation.class)) {
          for (CoreLabel token : sentence.get(TokensAnnotation.class)) {
            if (firstToken) {
              firstToken = false;
            } else {
              output.append("\t");
            }
            output.append(token.get(TextAnnotation.class)
                + " " + token.get(LemmaAnnotation.class)
                + " " + token.get(PartOfSpeechAnnotation.class));
          }
        }
        System.out.println(output.toString());
      } catch(Exception e) {
        System.err.println("i haz a sad " + e.getClass().getName()
            + " " + e.getMessage() + " [ " + text + "]");
      }
    }
  }
}
