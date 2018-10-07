package thealphaversion.app.safe_cide;

import android.content.Intent;
import android.net.Uri;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.widget.Button;
import android.net.Uri;
import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;

public class HelplineActivity extends AppCompatActivity {
    Button button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_helpline);


        //Getting the edittext and button instance
        //edittext1=(EditText)findViewById(R.id.editText1);
        button = (Button) findViewById(R.id.button);

        //Performing action on button click
        button.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View arg0) {
                String number="912227546669";
                Intent callIntent = new Intent(Intent.ACTION_CALL);
                callIntent.setData(Uri.parse("tel:" + number));
                startActivity(callIntent);
            }

        });
    }

}