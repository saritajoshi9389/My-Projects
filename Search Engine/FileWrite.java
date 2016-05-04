/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
// Program to write the query output and term frequency results to text file
package lucene.implementation;
import java.io.*;
import java.util.ArrayList;
import java.util.Map;
/**
 *
 * @author sarita joshi
 */
public class FileWrite {
    File file;
    public FileWrite(String filename)throws IOException{
        try
        {
      file = new File(filename);
      if (!file.exists()) 
      {
          file.createNewFile(); // Creates a new text file if it does not exist
      }
      // creates a FileWriter Object
   }
        catch (IOException e) {
			e.printStackTrace();
		}
} 
    // Function to write the top 100 Doc Ids along with scores to text file
    public void writeResults(ArrayList<String> results) throws IOException
    {
        BufferedWriter output = new BufferedWriter(new FileWriter(file));
        output.write("Top 100 Document Id, Document Name along with their scores (Decreasing Scores) :");
        output.newLine(); output.newLine();
        try
        {
        for (String result : results){
            output.write(result);
            output.newLine();}
            }catch ( IOException e ) {
            e.printStackTrace();
        } finally {
            if ( output != null ) output.close();
        }
    }
    
    /**
     *
     * @param values
     * @param results
     * @throws IOException
     */
    // Function to write term,term_frequency for all pairs in the given corpus
    public void writeTermFrequency(ArrayList<Map.Entry<String, Long>> values) throws IOException
    {
        BufferedWriter output = new BufferedWriter(new FileWriter(file));
        output.write("Term Frequency arranged in Sorted Order for all unique terms in corpus :");
        output.newLine(); output.newLine();
        output.write(String.format("%s   %-14s\t\t%-17s","RANK","TERM","FREQUENCY"));
        output.newLine();
        try
        {
        for (int i=0;i<values.size();i++)
        {
            String pair = values.get(i)+"";
            String[] splittedArr = pair.split("=");
            String word= splittedArr[0]; // Splits the Term and Frequency
            String freq = splittedArr[1];
            output.write(String.format("%d      %-14s\t\t%-17s",(i+1),word,freq));
            output.newLine();
        }
            }catch ( IOException e ) {
            e.printStackTrace();
        } finally {
            if ( output != null ) output.close();
        }
    }
    
}
    
