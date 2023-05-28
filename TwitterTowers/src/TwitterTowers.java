import java.util.Scanner;

public class TwitterTowers {

	public static void main(String[] args) {
		final int  RECTANGLE =1, TRIANGULAR =2, EXIT =3, PERIMETER = 1, PRINT = 2 ;
		Scanner scanner = new Scanner(System.in );
		int height = 0,width =0;
		int option = RECTANGLE;
		System.out.println("Twitter Towers");

		while(!(option == EXIT))
		{
			System.out.println("Please choose a tower\npress 1 for rectangle\npress 2 for triangular\npress 3 to exit");
			option = scanner.nextInt();
			if(option == EXIT)
			{
				System.out.println("Goodby");
				break;
			}
            if (option == RECTANGLE ||option == TRIANGULAR )
            {
            	// get the tower size
            	System.out.println("Enter please height.");
    			height = scanner.nextInt();
    			System.out.println("Enter please width.");
    			width = scanner.nextInt();
            }
			switch(option)
			{
			case RECTANGLE:
				if(Math.abs(height-width)>5)
					System.out.println("Tower area is "+ height*width);
				else
					System.out.println("Tower perimeter  is "+ (height+width)*2);
				break;
			case TRIANGULAR:
				System.out.println("Please choose an option: press 1 for perimeter press 2 to print");
				option = scanner.nextInt();
				if (option == PERIMETER)
				{
					// pythagorean theorem
					double c = Math.sqrt(Math.pow(height, 2) + Math.pow(width/2, 2));
					System.out.println("Tower perimeter  is "+ (c*2 + width));
				}
				else if (option == PRINT)
				{
					if(width%2 == 0 ||width > height*2)
					{
						System.out.println("Invalid dimensions for triangle");
						break;
					}
						// print the triangle 
						int innerRows = (width-2)/2; // number of the inner rows
						int printsPerLine = (height-2)/innerRows; // number of stars for inner line
						int firstLinePrints = (height-2)%innerRows + printsPerLine; // number of stars for the first inner line
						int nPrints = 1; // the current line number
						int nSpace; // the number of spaces in the beginning of the line
						for (int tmp=1, stars = 1, i = 1; i <= height; tmp++, stars+=2)
						{
							nSpace = height - tmp;
							if (i == 2)
								nPrints = firstLinePrints;
							else if(i!=1&&i< height-1 )
								nPrints = printsPerLine;
							else nPrints = 1;
							for(int j=1; j<=nPrints && i <= height;j++,i++)
							{	
								for (int sp = 1; sp <= nSpace; ++sp) 
								{
									System.out.print(" ");

								}
								for (int s = 1; s <= stars; ++s) 
								{
									System.out.print("*");
								}
								System.out.println();
							}
						}
					}
				break;
			default:
				System.out.println("Invalid  number");
				break;

			}
		}

	}

}

